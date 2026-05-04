from dataclasses import dataclass
from typing import Any

from ..pobject import POProperty
from . import color, draw, line, opacity

__all__ = ["CustomStyle", "color", "draw", "line", "opacity"]


@dataclass
class CustomStyle(POProperty):
    """
    Generic custom style parameter.

    Attributes:
        param: Name of the style parameter.
        value: Value associated with the parameter.
    """

    param: str
    value: Any

    def svg(self) -> str:
        return (
            f'{self.param}="{self.value:.4f}"'
            if isinstance(self.value, float)
            else f'{self.param}="{self.value}"'
        )

    def tikz(self) -> str:
        return f"{self.param}={self.value}"


@dataclass
class CustomProperty(POProperty):
    """
    Generic style with no associated value.

    Attributes:
        name: Name of the property.
    """

    name: str

    def svg(self) -> str:
        return f'{self.name}="none"'

    def tikz(self) -> str:
        return self.name
