"""How ``Unlok`` reaches the app's own lok: its links."""

from arkitekt_spec.declare.wiring import Alias, TokenLoader
from fakts.contrib.rath.auth import FaktsAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from rath.links.split import SplitLink

from graphql import OperationType
from unlok.rath import UnlokLinkComposition, UnlokRath


def unlok_rath(own: Alias, tokens: TokenLoader) -> UnlokRath:
    """The rath over http and ws."""
    return UnlokRath(
        link=UnlokLinkComposition(
            auth=FaktsAuthLink(token_loader=tokens),
            split=SplitLink(
                left=AIOHttpLink(
                    endpoint_url=own.to_http_path("graphql"),
                    proxy=own.proxy,
                    ssl_context=own.ssl_context(),
                ),
                right=GraphQLWSLink(
                    ws_endpoint_url=own.to_ws_path("graphql"),
                    proxy=own.proxy,
                    ssl_context=own.ssl_context(),
                ),
                split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
            ),
        )
    )


__all__ = ["unlok_rath"]
