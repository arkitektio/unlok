from pydantic import Field
from rath import rath
from rath.links.auth import AuthTokenLink
from rath.links.compose import TypedComposedLink
from rath.links.dictinglink import DictingLink
from rath.links.shrink import ShrinkingLink
from rath.links.split import SplitLink


class UnlokLinkComposition(TypedComposedLink):
    shrinking: ShrinkingLink = Field(default_factory=ShrinkingLink)
    dicting: DictingLink = Field(default_factory=DictingLink)
    auth: AuthTokenLink
    split: SplitLink


class UnlokRath(rath.Rath):
    """Unlok Rath

    The GraphQL client for unlok.

    Entering it does not make it "the current client": nothing is. It is the
    transport of the :class:`unlok.unlok.Unlok` client that owns it.
    """
