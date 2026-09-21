"""Test fixtures.

The integration fixtures start a real lok server (plus its database, redis and
object store) with docker compose through dokker, and authenticate the way a
deployed app does: the session *redeems* the token provisioned in the stack's
config through the fakts redeem grant, which enrols it as a development client
of the ``demo`` organisation. Everything the tests then do goes through that
client, so the whole path a container takes on start is under test, not just
the GraphQL layer.
"""

from __future__ import annotations

import os
import socket
import sys
from collections.abc import Generator
from dataclasses import dataclass

import pytest
from dokker import Deployment, testing
from dokker.log_watcher import LogWatcher
from fakts import Fakts
from rath.links.aiohttp import AIOHttpLink
from fakts.contrib.rath.auth import FaktsAuthLink
from rath.links.graphql_ws import GraphQLWSLink
from fakts.grants.remote.authorizers.redeem import RedeemAuthorizer
from fakts.grants.remote.base import RemoteGrant
from fakts.grants.remote.discovery.well_known import WellKnownDiscovery
from fakts.models import Manifest
from graphql import OperationType
from rath.links.split import SplitLink

from unlok.rath import UnlokLinkComposition, UnlokRath
from unlok.unlok import Unlok


def pytest_configure(config: pytest.Config) -> None:
    """Register custom platform markers."""
    config.addinivalue_line("markers", "linux_only: skip on non-Linux platforms")
    config.addinivalue_line("markers", "no_windows: skip on Windows")


def pytest_collection_modifyitems(config: pytest.Config, items: list) -> None:
    """Skip tests marked linux_only or no_windows on the wrong platform."""
    for item in items:
        if item.get_closest_marker("linux_only") and sys.platform != "linux":
            item.add_marker(pytest.mark.skip(reason="Linux only"))
        if item.get_closest_marker("no_windows") and sys.platform == "win32":
            item.add_marker(pytest.mark.skip(reason="Not supported on Windows"))


project_path = os.path.join(os.path.dirname(__file__), "integration")
docker_compose_file = os.path.join(project_path, "docker-compose.yml")
# An untracked sibling override (see its own header): when a developer's checkout sits next
# to a live lok source tree, it builds the lok image from that tree instead of pulling the
# published one, so the tests see the current schema rather than the last-pushed one.
# Absent (CI, anyone else), the published image is the schema under test.
_local_override = os.path.join(project_path, "docker-compose.local.yml")
compose_files = [docker_compose_file] + ([_local_override] if os.path.exists(_local_override) else [])

# What tests/integration/configs/lok.yaml provisions: the token is issued for the
# `localhost` hub of the `demo` organisation, never expires and may be redeemed any
# number of times, so every test session (and every retry) can enrol with it.
STACK_REDEEM_TOKEN = "unlok-integration-tests-redeem-token"

TEST_MANIFEST = Manifest(
    identifier="live.arkitekt.unlok_tests",
    version="0.0.1",
    scopes=[],
    requirements=[],
    node_id="unlok-integration-tests",
)


def _reserve_free_ports(count: int) -> list[int]:
    """Ask the OS for `count` distinct free TCP ports.

    All sockets are held open until every port has been assigned, so the kernel
    cannot hand out the same port twice within one call. They are released
    before compose binds them -- a race in theory, but the ephemeral range is
    large and this is what keeps concurrent runs (and the leftovers of a crashed
    one) from colliding on a fixed port.
    """
    sockets: list[socket.socket] = []
    try:
        for _ in range(count):
            sock = socket.socket()
            sock.bind(("127.0.0.1", 0))
            sockets.append(sock)
        return [int(sock.getsockname()[1]) for sock in sockets]
    finally:
        for sock in sockets:
            sock.close()


@pytest.fixture(scope="session")
def integration_ports() -> Generator[dict[str, int], None, None]:
    """Pick this run's host ports and point compose at them.

    Reserved rather than left to docker (`ports: - "80"`) because
    `Deployment.spec` is rendered by `docker compose config`, which is static:
    an unpublished port reads back as ``None`` and the test URLs would quietly
    become ``http://localhost:None`` instead of failing loudly.
    """
    lok_port, rustfs_port = _reserve_free_ports(2)
    env = {"LOK_HOST_PORT": str(lok_port), "RUSTFS_HOST_PORT": str(rustfs_port)}
    previous = {key: os.environ.get(key) for key in env}
    os.environ.update(env)
    try:
        yield {"lok": lok_port, "rustfs": rustfs_port}
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def build_redeeming_fakts(base_url: str, token: str, manifest: Manifest) -> Fakts:
    """A fakts client that authenticates by redeeming ``token`` for ``manifest``.

    This is what a deployed container does on start (``arkitekt run prod`` with
    ``FAKTS_REDEEM_TOKEN``), minus the on-disk cache: the tests want every
    session to go through the grant.
    """
    return Fakts(
        grant=RemoteGrant(
            authorizer=RedeemAuthorizer(token=token, manifest=manifest, allow_insecure_transport=True),
            discovery=WellKnownDiscovery(url=base_url, allow_insecure_transport=True),
        ),
        manifest=manifest,
        allow_insecure_transport=True,
    )


def build_unlok(fakts: Fakts) -> Unlok:
    """The unlok client over a fakts session, composed like ``unlok.arkitekt.unlok``.

    Resolved once, here, exactly as a run resolves it: the service talks to the
    app's own fakts server, so the address is the self alias. Kept in sync with
    the service by hand because this is the sync path and the service builds
    asynchronously.
    """
    own = fakts.get_self_alias()
    return Unlok(
        rath=UnlokRath(
            link=UnlokLinkComposition(
                auth=FaktsAuthLink(token_loader=fakts),
                split=SplitLink(
                    left=AIOHttpLink(endpoint_url=own.to_http_path("graphql")),
                    right=GraphQLWSLink(ws_endpoint_url=own.to_ws_path("graphql")),
                    split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                ),
            )
        )
    )


@dataclass
class DeployedUnlok:
    """The deployed lok stack and a client enrolled into it."""

    deployment: Deployment
    lok_watcher: LogWatcher
    base_url: str
    """Where lok is served for this run, e.g. ``http://localhost:41234/lok``."""
    fakts: Fakts
    unlok: Unlok


@pytest.fixture(scope="session")
def deployed_app(integration_ports: dict[str, int]) -> Generator[DeployedUnlok, None, None]:
    """Deploy the lok stack with Docker Compose and enrol a client into it.

    Yields:
        DeployedUnlok: the deployment, a log watcher for lok, the base URL, and the
        fakts session + unlok client the tests act through.

    """
    setup = testing(compose_files)
    setup.add_health_check(
        url=lambda spec: f"http://localhost:{spec.find_service('lok').get_port_for_internal(80).published}/lok/ht",
        service="lok",
        timeout=5,
        max_retries=40,
    )
    watcher = setup.create_watcher("lok")

    with setup:
        # dokker >= 2.6 does nothing on enter: the spec below has to be resolved
        # explicitly. `up()` (testing policy) also reaps stacks earlier, since-killed
        # test runs left behind and labels this one with our PID.
        setup.down()
        if os.path.exists(_local_override):
            setup.build("lok")
        else:
            setup.pull()
        setup.inspect()

        base_url = f"http://localhost:{setup.spec.find_service('lok').get_port_for_internal(80).published}/lok"

        setup.up()
        setup.check_health()

        fakts = build_redeeming_fakts(base_url, STACK_REDEEM_TOKEN, TEST_MANIFEST)
        with fakts:
            with build_unlok(fakts) as unlok:
                yield DeployedUnlok(
                    deployment=setup,
                    lok_watcher=watcher,
                    base_url=base_url,
                    fakts=fakts,
                    unlok=unlok,
                )


@pytest.fixture(scope="session")
def unlok(deployed_app: DeployedUnlok) -> Unlok:
    """The deployment's client: API calls are its methods, nothing is ambient."""
    return deployed_app.unlok
