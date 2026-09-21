"""The deployer's credential flow, end to end against a real lok.

A pinned redeem token is minted by an enrolled client, handed to a *second* fakts
session standing in for the container, redeemed there, checked, and spent. Every
step goes through the real grant at ``/o/token/``; nothing is mocked.
"""

import pytest
from fakts.grants.remote.errors import RetrieveError
from fakts.models import Manifest

from unlok.api.schema import ManifestInput
from unlok.unlok import Unlok

from .conftest import DeployedUnlok, build_redeeming_fakts

PINNED = ManifestInput(identifier="com.example.pinned", version="1.0.0", scopes=[], node_id="node-a")


def _manifest(**overrides: object) -> Manifest:
    fields = {"identifier": "com.example.pinned", "version": "1.0.0", "scopes": [], "requirements": [], "device_id": "node-a"}
    fields.update(overrides)
    return Manifest(**fields)


@pytest.mark.integration
def test_minted_token_is_pinned_and_unredeemed(deployed_app: DeployedUnlok, unlok: Unlok) -> None:
    """A token minted by an app carries its pin and no client yet."""
    token = unlok.create_redeem_token(manifest=PINNED, expires_in_days=1, max_redemptions=1)

    assert token.pinned_manifest["identifier"] == "com.example.pinned"
    assert token.pinned_manifest["version"] == "1.0.0"
    assert token.pinned_manifest["device_id"] == "node-a"
    assert token.max_redemptions == 1
    assert token.redemption_count == 0
    assert token.client is None
    assert token.expires_at is not None


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
def test_pinned_token_refuses_a_deviating_manifest(deployed_app: DeployedUnlok, unlok: Unlok, deviation: dict, fragment: str) -> None:
    """The container cannot enrol as anything but the approved app."""
    token = unlok.create_redeem_token(manifest=PINNED, expires_in_days=1)

    with build_redeeming_fakts(deployed_app.base_url, token.token, _manifest(**deviation)) as impostor:
        with pytest.raises(RetrieveError, match=fragment):
            impostor.get_self_alias()

    after = unlok.redeem_token(token.id)
    assert after.client is None, "a refused redeem must not provision a client"
    assert after.redemption_count == 0


@pytest.mark.integration
def test_pinned_token_is_redeemed_verified_and_spent(deployed_app: DeployedUnlok, unlok: Unlok) -> None:
    """The happy path a deployer drives: mint, let the container redeem, verify, delete."""
    token = unlok.create_redeem_token(manifest=PINNED, expires_in_days=1, max_redemptions=1)

    # The "container" redeems it and gets a working session.
    with build_redeeming_fakts(deployed_app.base_url, token.token, _manifest()) as container:
        alias = container.get_self_alias()
        assert alias.to_http_path("graphql").startswith(deployed_app.base_url)

    # The deployer sees which client the token produced and checks it is the approved app.
    redeemed = unlok.redeem_token(token.id)
    assert redeemed.client is not None
    assert redeemed.client.release.app.identifier == "com.example.pinned"
    assert redeemed.client.release.version == "1.0.0"
    assert redeemed.client.client_id
    assert redeemed.redemption_count == 1

    # Then it spends the token: gone for the deployer ...
    assert unlok.delete_redeem_token(token.id) == token.id
    with pytest.raises(Exception, match="not authorized"):
        unlok.redeem_token(token.id)

    # ... and worthless for anyone who read it out of the container's environment.
    with build_redeeming_fakts(deployed_app.base_url, token.token, _manifest()) as thief:
        with pytest.raises(RetrieveError, match="Invalid redeem token"):
            thief.get_self_alias()


@pytest.mark.integration
def test_single_use_token_cannot_be_redeemed_twice(deployed_app: DeployedUnlok, unlok: Unlok) -> None:
    """``maxRedemptions: 1`` closes the window between redeem and revocation."""
    token = unlok.create_redeem_token(manifest=PINNED, expires_in_days=1, max_redemptions=1)

    with build_redeeming_fakts(deployed_app.base_url, token.token, _manifest()) as first:
        first.get_self_alias()

    with build_redeeming_fakts(deployed_app.base_url, token.token, _manifest()) as second:
        with pytest.raises(RetrieveError, match="maximum number of times"):
            second.get_self_alias()
