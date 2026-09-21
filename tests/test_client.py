"""An unlok call goes through the client it is made on, and nothing else.

No server: the rath is a fake returning canned data.
"""

from types import SimpleNamespace
from typing import Any, AsyncIterator, Optional

import pytest
from koil import Koil
from pydantic import BaseModel, ConfigDict
from rath.links.testing.mock import AsyncMockLink
from rath.origin import ContextBound, get_origin

from unlok.api.schema import UnlokApi
from unlok.rath import UnlokRath
from unlok.unlok import Unlok


class FakeRath:
    """Answers every query with the same canned service, and remembers what was sent."""

    def __init__(self) -> None:
        self.sent: list[dict[str, Any]] = []

    def _answer(self, variables: dict[str, Any]) -> Any:
        self.sent.append(variables)
        return SimpleNamespace(data={"service": {"id": "service-1", "owner": {"id": "u-1"}}})

    async def aquery(self, document: str, variables: dict[str, Any]) -> Any:
        return self._answer(variables)

    async def asubscribe(self, document: str, variables: dict[str, Any]) -> AsyncIterator[Any]:
        yield self._answer(variables)


class Owner(ContextBound):
    model_config = ConfigDict(frozen=True)
    id: str


class Service(ContextBound):
    model_config = ConfigDict(frozen=True)
    id: str
    owner: Owner


class GetService(BaseModel):
    """Shaped like a generated operation."""

    service: Service

    class Arguments(BaseModel):
        id: str
        note: Optional[str] = None

    class Meta:
        document = "query GetService($id: ID!) { service(id: $id) { id owner { id } } }"


def client() -> Any:
    """The real client over a fake rath, built without validating the rath's type."""
    return Unlok.model_construct(rath=FakeRath())


@pytest.mark.asyncio
async def test_aexecute_goes_through_the_client_and_results_remember_it() -> None:
    mine, other = client(), client()

    result = await mine.aexecute(GetService, {"id": "service-1"})

    assert (len(mine.rath.sent), len(other.rath.sent)) == (1, 0)
    origin = get_origin(result.service.owner)
    assert origin is not None and origin.client is mine and origin.rath is mine.rath


def test_execute_goes_through_the_client() -> None:
    mine = client()
    with Koil():
        assert mine.execute(GetService, {"id": "service-1"}).service.id == "service-1"
    assert len(mine.rath.sent) == 1


@pytest.mark.asyncio
async def test_asubscribe_goes_through_the_client() -> None:
    mine = client()
    events = [e async for e in mine.asubscribe(GetService, {"id": "service-1"})]
    assert [e.service.id for e in events] == ["service-1"]
    assert get_origin(events[0].service).client is mine


def test_subscribe_goes_through_the_client() -> None:
    mine = client()
    with Koil():
        events = list(mine.subscribe(GetService, {"id": "service-1"}))
    assert [e.service.id for e in events] == ["service-1"]
    assert len(mine.rath.sent) == 1


@pytest.mark.asyncio
async def test_unset_arguments_are_left_out() -> None:
    """unlok's wire behaviour, kept through the rewrite: exclude_unset.

    An argument the caller did not set is absent, so the server applies the
    schema's default rather than rejecting a ``null``.
    """
    mine = client()
    await mine.aexecute(GetService, {"id": "service-1"})
    await mine.aexecute(GetService, {"id": "service-1", "note": None})
    assert mine.rath.sent == [{"id": "service-1"}, {"id": "service-1", "note": None}]


def test_every_operation_is_a_method_of_the_client() -> None:
    service = Unlok(rath=UnlokRath(link=AsyncMockLink()))

    assert isinstance(service, UnlokApi)
    assert callable(service.aget_service) and callable(service.list_services)
    # A kontext that answers for itself, so actions can be handed it.


@pytest.mark.asyncio
async def test_a_generated_method_delegates_to_its_own_aexecute(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import unlok.api.schema as schema

    seen: list[Any] = []

    async def fake_aexecute(self: Any, operation: Any, variables: Any) -> Any:
        seen.append((self, operation, variables))
        return SimpleNamespace(service="the-service")

    monkeypatch.setattr(Unlok, "aexecute", fake_aexecute)
    service = Unlok(rath=UnlokRath(link=AsyncMockLink()))

    assert await service.aget_service("service-1") == "the-service"
    ((passed, operation, variables),) = seen
    assert passed is service
    assert operation is schema.GetServiceQuery and variables == {"id": "service-1"}
