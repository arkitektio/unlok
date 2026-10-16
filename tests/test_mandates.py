"""Agent mandates, end to end against a real lok.

A grantor lets an agent app issue keys for a subject app that log in as the
grantor. Here the test client is both: it grants the mandate naming its own app
as the agent, so the same session may issue under it. Each key then logs a
second fakts session in, standing in for a started app.
"""

import uuid

import pytest
from fakts.errors import NeedsReauthenticationError
from fakts.models import Manifest
from rath.operation import GraphQLException

from unlok.api.schema import ManifestInput
from unlok.unlok import Unlok

from .conftest import TEST_MANIFEST, DeployedUnlok, build_key_fakts

SUBJECT = ManifestInput(identifier="com.example.mandated", version="1.0.0", scopes=[])


def _subject(device_id: str) -> Manifest:
    return Manifest(identifier="com.example.mandated", version="1.0.0", scopes=[], requirements=[], device_id=device_id)


def _mandate(unlok: Unlok, max_clients: int = 1):
    return unlok.create_mandate(agent=TEST_MANIFEST.identifier, manifest=SUBJECT, max_clients=max_clients, expires_in_days=1)


def _device() -> str:
    return f"host-a:{uuid.uuid4().hex[:8]}"


@pytest.mark.integration
def test_a_mandate_pins_its_subject_and_is_listed(unlok: Unlok) -> None:
    mandate = _mandate(unlok)

    assert mandate.agent_identifier == TEST_MANIFEST.identifier
    assert mandate.subject.identifier == "com.example.mandated"
    assert mandate.subject.device_id is None
    assert mandate.max_clients == 1
    assert mandate.is_live
    assert unlok.get_mandate(mandate.id).id == mandate.id
    assert mandate.id in [m.id for m in unlok.list_mandates()]


@pytest.mark.integration
def test_a_child_key_logs_the_subject_in(deployed_app: DeployedUnlok, unlok: Unlok) -> None:
    mandate = _mandate(unlok)
    device = _device()

    child = unlok.issue_child_mandate_key(mandate.id, device_id=device)
    assert child.key
    assert child.mandate.parent.id == mandate.id
    assert child.mandate.subject.device_id == device

    # The started app logs in with it, as FAKTS_MANDATE_KEY would.
    with build_key_fakts(deployed_app.base_url, child.key, _subject(device)) as app:
        app.get_self_alias()

    seen = unlok.get_mandate(child.mandate.id)
    assert len(seen.clients) == 1


@pytest.mark.integration
def test_max_clients_counts_live_children_and_revoking_one_frees_a_slot(deployed_app: DeployedUnlok, unlok: Unlok) -> None:
    mandate = _mandate(unlok, max_clients=1)
    first = unlok.issue_child_mandate_key(mandate.id, device_id=_device())

    with pytest.raises(GraphQLException, match="no slots"):
        unlok.issue_child_mandate_key(mandate.id, device_id=_device())

    unlok.revoke_mandate(first.mandate.id)
    assert unlok.issue_child_mandate_key(mandate.id, device_id=_device()).key


@pytest.mark.integration
def test_revoking_the_mandate_kills_every_key_issued_under_it(deployed_app: DeployedUnlok, unlok: Unlok) -> None:
    mandate = _mandate(unlok)
    device = _device()
    child = unlok.issue_child_mandate_key(mandate.id, device_id=device)

    revoked = unlok.revoke_mandate(mandate.id)
    assert revoked.is_live is False
    assert revoked.revoked_at is not None

    with build_key_fakts(deployed_app.base_url, child.key, _subject(device)) as app:
        with pytest.raises(NeedsReauthenticationError):
            app.get_self_alias()
    with pytest.raises(GraphQLException):
        unlok.issue_child_mandate_key(mandate.id, device_id=_device())
