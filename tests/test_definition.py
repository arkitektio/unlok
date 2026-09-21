"""Smoke test: the enrolled client can talk to lok at all."""

import pytest

from unlok.unlok import Unlok


@pytest.mark.integration
def test_enrolled_client_can_query(unlok: Unlok) -> None:
    """The session redeemed the stack's token and holds a working client.

    The test hub offers no services, so an empty tuple is the correct answer; what
    is under test is that the query is authenticated and answered at all.
    """
    services = unlok.list_services()

    assert isinstance(services, tuple)
