from types import ModuleType

from . import meteoprog
from . import meteofor


def get_weather_provider_module_by_(name: str) -> ModuleType:
    """Returns weather provider module by the given name."""
    return {"meteoprog": meteoprog, "meteofor": meteofor}.get(name)
