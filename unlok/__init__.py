# The service is declared with arkitekt-spec, a core dependency: it is always there.
from .arkitekt import unlok as unlok_service
from .unlok import Unlok

__all__ = ["Unlok", "unlok_service"]
