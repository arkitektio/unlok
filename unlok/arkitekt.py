"""The unlok service of an arkitekt app, and the types it sends by id.

Declared on one registry: the service first, then the structures whose expanders
ask for the client it returns. An app takes all of it in with
``App(services=[unlok_service])``.
"""

import os
from typing import Annotated

from fakts import Alias, Own, TokenLoader
from fakts.contrib.rath.auth import FaktsAuthLink
from graphql import OperationType
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from rath.links.split import SplitLink

from rekuest.app import AppRegistry

from unlok.api.schema import Service
from unlok.rath import UnlokLinkComposition, UnlokRath
from unlok.unlok import Unlok


def build_relative_path(*path: str) -> str:
    """Build a path relative to this file, for the files shipped beside it."""
    return os.path.join(os.path.dirname(__file__), *path)


registry = AppRegistry()
"""What unlok brings to an app: its service, and the types it can send by id."""


@registry.service(
    schema=build_relative_path("api", "schema.graphql"),
    turms=build_relative_path("api", "project.json"),
)
def unlok(own: Annotated[Alias, Own()], tokens: TokenLoader) -> Unlok:
    """Unlok: users, groups and the app's own identity.

    The one service that requires nothing. It talks to the app's *own* fakts
    server rather than to a service a deployment composes for it, so there is
    nothing to provision and nothing to declare.
    """
    return Unlok(
        rath=UnlokRath(
            link=UnlokLinkComposition(
                auth=FaktsAuthLink(token_loader=tokens),
                split=SplitLink(
                    left=AIOHttpLink(endpoint_url=own.to_http_path("graphql")),
                    right=GraphQLWSLink(ws_endpoint_url=own.to_ws_path("graphql")),
                    split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                ),
            )
        )
    )


@registry.structure("@lok/service")
async def expand_service(id: str, unlok: Unlok) -> Service:
    """A service, by id. It travels as `@lok/service`, not `@unlok/...`."""
    return await unlok.aget_service(id)
