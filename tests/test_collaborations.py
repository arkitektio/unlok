"""Collaborations, end to end against a real lok: lok owns them, every service names one by its key."""

import pytest

from unlok.api.schema import CollaborationFilter
from unlok.unlok import Unlok


@pytest.mark.integration
def test_a_collaboration_is_found_by_its_id_and_its_key(unlok: Unlok) -> None:
    created = unlok.create_collaboration(
        name="Shared imaging", description="for guests"
    )

    assert created.key
    assert created.name == "Shared imaging"
    assert created.description == "for guests"
    assert unlok.get_collaboration(id=created.id).key == created.key
    assert unlok.get_collaboration(key=created.key).id == created.id
    listed = unlok.list_collaborations(filters=CollaborationFilter(keys=(created.key,)))
    assert [c.id for c in listed] == [created.id]


@pytest.mark.integration
def test_a_collaboration_is_renamed_and_deleted(unlok: Unlok) -> None:
    created = unlok.create_collaboration(name="Before")

    renamed = unlok.update_collaboration(id=created.id, name="After")
    assert renamed.name == "After"
    assert renamed.key == created.key

    assert unlok.delete_collaboration(created.id) == created.id
    assert created.id not in [c.id for c in unlok.list_collaborations()]
