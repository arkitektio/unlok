"""Mandates, end to end against a real lok.

A grantor lets an agent app provision clients of a subject app that act as the
grantor. Here the test client is both: it grants the mandate naming its own app
as the agent, so the same session may provision under it. The provisioned token
is then redeemed by a second fakts session standing in for the started app.
"""

import uuid

import pytest
from fakts.models import Manifest
from rath.operation import GraphQLException

from unlok.api.schema import ManifestInput
from unlok.unlok import Unlok

from .conftest import TEST_MANIFEST, DeployedUnlok, build_redeeming_fakts

SUBJECT = ManifestInput(identifier="com.example.mandated", version="1.0.0", scopes=[])


def _subject(device_id: str) -> Manifest:
    return Manifest(
        identifier="com.example.mandated",
        version="1.0.0",
        scopes=[],
        requirements=[],
        device_id=device_id,
    )


def _mandate(unlok: Unlok, max_clients: int = 1):
    return unlok.create_mandate(
        agent=TEST_MANIFEST.identifier,
        manifest=SUBJECT,
        max_clients=max_clients,
        expires_in_days=1,
    )


@pytest.mark.integration
def test_a_mandate_pins_its_subject_and_is_listed(unlok: Unlok) -> None:
    mandate = _mandate(unlok)

    assert mandate.agent_identifier == TEST_MANIFEST.identifier
    assert mandate.subject_manifest["identifier"] == "com.example.mandated"
    assert mandate.max_clients == 1
    assert mandate.is_live
    assert unlok.get_mandate(mandate.id).id == mandate.id
    assert mandate.id in [m.id for m in unlok.list_mandates()]


@pytest.mark.integration
def test_a_provisioned_token_enrols_the_subject(deployed_app: DeployedUnlok, unlok: Unlok) -> None:
    mandate = _mandate(unlok)
    device = f"host-a:{uuid.uuid4().hex[:8]}"

    token = unlok.provision(mandate.id, device_id=device)
    assert token.token
    assert token.mandate.id == mandate.id
    assert token.pinned_manifest["device_id"] == device

    # The started app redeems it, as FAKTS_REDEEM_TOKEN would.
    with build_redeeming_fakts(deployed_app.base_url, token.token, _subject(device)) as app:
        app.get_self_alias()

    # The agent sees which client its token produced.
    seen = unlok.mandate_token(token.id)
    assert seen.client is not None
    assert seen.client.release.app.identifier == "com.example.mandated"


@pytest.mark.integration
def test_max_clients_is_enforced_and_release_frees_a_slot(deployed_app: DeployedUnlok, unlok: Unlok) -> None:
    mandate = _mandate(unlok, max_clients=1)
    first_device = f"host-a:{uuid.uuid4().hex[:8]}"
    first = unlok.provision(mandate.id, device_id=first_device)

    with pytest.raises(GraphQLException, match="no client slots"):
        unlok.provision(mandate.id, device_id=f"host-a:{uuid.uuid4().hex[:8]}")

    with build_redeeming_fakts(deployed_app.base_url, first.token, _subject(first_device)) as app:
        app.get_self_alias()
    client = unlok.mandate_token(first.id).client
    assert client is not None

    unlok.release_mandate_client(client.client_id)
    assert unlok.provision(mandate.id, device_id=f"host-a:{uuid.uuid4().hex[:8]}").token


@pytest.mark.integration
def test_a_revoked_mandate_provisions_nothing(unlok: Unlok) -> None:
    mandate = _mandate(unlok)

    revoked = unlok.revoke_mandate(mandate.id)
    assert revoked.is_live is False
    assert revoked.revoked_at is not None

    with pytest.raises(GraphQLException):
        unlok.provision(mandate.id, device_id=f"host-a:{uuid.uuid4().hex[:8]}")
