"""The types unlok sends by id: each expanded by the ``Unlok`` client.

Imported by ``unlok/__init__``, so each class is marked whenever unlok is.
"""

from arkitekt_spec.declare.structures.declare import structure

from unlok.api.schema import Service
from unlok.unlok import Unlok


@structure("@lok/service")
async def expand_service(id: str, unlok: Unlok) -> Service:
    """A service, by id. It travels as `@lok/service`, not `@unlok/...`."""
    return await unlok.aget_service(id)
