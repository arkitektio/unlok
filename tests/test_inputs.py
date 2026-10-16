"""Unit tests for the generated input models: no server involved.

They pin the wire shape an issuer relies on -- the manifest and the expiry are
mandatory when an app issues a key, and every field travels under its GraphQL
(camelCase) name.
"""

import pytest
from pydantic import ValidationError

from unlok.api.schema import IssueMandateKeyInput, ManifestInput, RequirementInput


def test_an_app_issued_key_needs_a_manifest_and_an_expiry() -> None:
    with pytest.raises(ValidationError, match="manifest"):
        IssueMandateKeyInput(expires_in_days=1)  # type: ignore[call-arg]
    with pytest.raises(ValidationError, match="expires_in_days|expiresInDays"):
        IssueMandateKeyInput(manifest=ManifestInput(identifier="a", version="1"))  # type: ignore[call-arg]


def test_issue_mandate_key_input_serializes_under_graphql_names() -> None:
    """Snake-case attributes go out as the camelCase the schema declares."""
    manifest = ManifestInput(
        identifier="com.example.app",
        version="1.0.0",
        scopes=["read"],
        node_id="node-a",
        requirements=[
            RequirementInput(key="rekuest", service="live.arkitekt.rekuest", optional=False)
        ],
    )

    wire = IssueMandateKeyInput(manifest=manifest, expires_in_days=1, max_clients=1).model_dump(
        by_alias=True, exclude_none=True
    )

    assert wire["manifest"] == {
        "identifier": "com.example.app",
        "version": "1.0.0",
        "scopes": ("read",),
        "nodeId": "node-a",
        "requirements": (
            {"key": "rekuest", "service": "live.arkitekt.rekuest", "optional": False},
        ),
    }
    assert wire["expiresInDays"] == 1
    assert wire["maxClients"] == 1
