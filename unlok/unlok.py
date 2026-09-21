"""The base client for unlok"""

from collections.abc import AsyncGenerator, Generator
from typing import Any

from koil import unkoil, unkoil_gen
from koil.composition import Composition
from pydantic import Field
from rath.origin import origin_context
from rath.turms.funcs import TOperation

from unlok.api.schema import UnlokApi
from unlok.rath import UnlokRath


class Unlok(Composition, UnlokApi):
    """Unlok

    Every unlok operation is a method of it (``unlok.aget_service(id)``). Actions
    ask for it by annotation (``unlok: Unlok``) and are handed their app's client.

    Each generated method hands its operation class and variables to ``execute``/
    ``aexecute`` (queries and mutations) or ``subscribe``/``asubscribe``
    (subscriptions) below, which run it over ``rath``. Nothing is looked up, and
    what a call returns remembers the client it was called on.
    """

    rath: UnlokRath = Field(
        ...,
        description="The Rath client used to interact with the lok API.",
    )

    @staticmethod
    def _serialize(operation: type[TOperation], variables: dict[str, Any]) -> dict[str, Any]:
        """The variables as sent on the wire.

        Arguments are serialised with ``exclude_unset=True``: an input field the
        caller did not provide is left out of the variables rather than sent as
        ``null``, so the server applies the default the schema declares for it
        (``requirements: [] = []`` on a manifest, say). Sending ``null`` for a
        non-nullable defaulted field is a validation error on the server, which is
        what happened before this was added.
        """
        return operation.Arguments(**variables).model_dump(by_alias=True, exclude_unset=True)

    def execute(self, operation: type[TOperation], variables: dict[str, Any]) -> TOperation:
        """Executes a query or mutation in a blocking way."""
        return unkoil(self.aexecute, operation, variables)

    async def aexecute(self, operation: type[TOperation], variables: dict[str, Any]) -> TOperation:
        """Executes a query or mutation in a non-blocking way."""
        x = await self.rath.aquery(operation.Meta.document, self._serialize(operation, variables))
        return operation.model_validate(x.data, context=origin_context(client=self, rath=self.rath))

    def subscribe(
        self, operation: type[TOperation], variables: dict[str, Any]
    ) -> Generator[TOperation, None, None]:
        """Subscribes to an operation in a blocking way."""
        return unkoil_gen(self.asubscribe, operation, variables)

    async def asubscribe(
        self, operation: type[TOperation], variables: dict[str, Any]
    ) -> AsyncGenerator[TOperation, None]:
        """Subscribes to an operation in a non-blocking way."""
        async for event in self.rath.asubscribe(
            operation.Meta.document, self._serialize(operation, variables)
        ):
            yield operation.model_validate(
                event.data, context=origin_context(client=self, rath=self.rath)
            )
