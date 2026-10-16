"""Mandate keys, end to end against a real lok.

The enrolled session issues a key for an app, and a *second* fakts session
standing in for the container logs in with it. Every step goes through the real
grant at ``/o/token/``; nothing is mocked.
"""

import pytest
from fakts.errors import NeedsReauthenticationError
from fakts.models import Manifest

from unlok.api.schema import ManifestInput
from unlok.unlok import Unlok

from .conftest import STACK_MANDATE_KEY, DeployedUnlok, build_key_fakts

PINNED = ManifestInput(identifier="com.example.pinned", version="1.0.0", scopes=[], node_id="node-a")


def _manifest(**overrides: object) -> Manifest:
    fields = {"identifier": "com.example.pinned", "version": "1.0.0", "scopes": [], "requirements": [], "device_id": "node-a"}
    fields.update(overrides)
    return Manifest(**fields)


@pytest.mark.integration
def test_an_issued_key_is_pinned_and_shown_once(deployed_app: DeployedUnlok, unlok: Unlok) -> None:
    issued = unlok.issue_mandate_key(manifest=PINNED, expires_in_days=1, max_clients=1, any_version=False, allow_mesh=False)

    assert len(issued.key) >= 32
    assert issued.key.startswith(issued.mandate.key_prefix)
    assert issued.mandate.subject.identifier == "com.example.pinned"
    assert issued.mandate.subject.version == "1.0.0"
    assert issued.mandate.subject.device_id == "node-a"
    assert issued.mandate.max_clients == 1
    assert issued.mandate.clients == ()
    assert issued.mandate.expires_at is not None


@pytest.mark.integration
@pytest.mark.parametrize(
    "deviation, fragment",
    [
        ({"identifier": "com.example.other"}, "pinned to app"),
        ({"version": "2.0.0"}, "pinned to version"),
        ({"device_id": "node-b"}, "different device"),
        ({"scopes": ["write"]}, "does not authorize the scope"),
    ],
)
def test_a_key_refuses_a_deviating_manifest(deployed_app: DeployedUnlok, unlok: Unlok, deviation: dict, fragment: str) -> None:
    """The container cannot log in as anything but the approved app."""
    issued = unlok.issue_mandate_key(manifest=PINNED, expires_in_days=1, any_version=False, allow_mesh=False)

    with build_key_fakts(deployed_app.base_url, issued.key, _manifest(**deviation)) as impostor:
        with pytest.raises(NeedsReauthenticationError, match=fragment):
            impostor.get_self_alias()

    assert unlok.get_mandate(issued.mandate.id).clients == (), "a refused login must not provision a client"


@pytest.mark.integration
def test_a_key_logs_in_again_as_the_same_client_until_revoked(deployed_app: DeployedUnlok, unlok: Unlok) -> None:
    """What a deployer drives: issue, let the container log in (and restart), revoke."""
    issued = unlok.issue_mandate_key(manifest=PINNED, expires_in_days=1, any_version=False, allow_mesh=False)

    with build_key_fakts(deployed_app.base_url, issued.key, _manifest()) as container:
        alias = container.get_self_alias()
        assert alias.to_http_path("graphql").startswith(deployed_app.base_url)
        assert container.loaded_fakts.auth.refresh_token is None
        first_client = container.loaded_fakts.auth.client_id
    with build_key_fakts(deployed_app.base_url, issued.key, _manifest()) as restarted:
        restarted.get_self_alias()
        assert restarted.loaded_fakts.auth.client_id == first_client

    seen = unlok.get_mandate(issued.mandate.id)
    assert [c.client_id for c in seen.clients] == [first_client]

    revoked = unlok.revoke_mandate(issued.mandate.id)
    assert revoked.is_live is False
    assert revoked.clients == ()
    with build_key_fakts(deployed_app.base_url, issued.key, _manifest()) as thief:
        with pytest.raises(NeedsReauthenticationError, match="revoked"):
            thief.get_self_alias()


@pytest.mark.integration
def test_the_configured_key_logs_an_app_in(deployed_app: DeployedUnlok) -> None:
    manifest = Manifest(identifier="com.example.configured", version="1.0.0", scopes=[], requirements=[])
    with build_key_fakts(deployed_app.base_url, STACK_MANDATE_KEY, manifest) as app:
        app.get_self_alias()
        assert app.loaded_fakts.auth.client_id
