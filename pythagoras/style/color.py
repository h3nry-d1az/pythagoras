"""
`Color` RGB container and predefined color constants. Included colors:

- ``BLACK``: (0, 0, 0).
- ``WHITE``: (255, 255, 255).
- ``RED``: (255, 0, 0).
- ``LIME``: (0, 255, 0).
- ``BLUE``: (0, 0, 255).
- ``YELLOW``: (255, 255, 0).
- ``CYAN``: (0, 255, 255).
- ``MAGENTA``: (255, 0, 255).
- ``SILVER``: (192, 192, 192).
- ``GRAY``: (128, 128, 128).
- ``MAROON``: (128, 0, 0).
- ``OLIVE``: (128, 128, 0).
- ``GREEN``: (0, 128, 0).
- ``PURPLE``: (128, 0, 128).
- ``TEAL``: (0, 128, 128).
- ``NAVY``: (0, 0, 128).
- ``ORANGE``: (255, 165, 0).
- ``PINK``: (255, 192, 203).
- ``BROWN``: (165, 42, 42).
- ``GOLD``: (255, 215, 0).
- ``INDIGO``: (75, 0, 130).
- ``VIOLET``: (238, 130, 238).
- ``BEIGE``: (245, 245, 220).
- ``TURQUOISE``: (64, 224, 208).
- ``CORAL``: (255, 127, 80).
- ``LIGHT_RED``: (255, 128, 128).
- ``LIGHT_BLUE``: (173, 216, 230).
- ``LIGHT_GREEN``: (144, 238, 144).
- ``LIGHT_CYAN``: (224, 255, 255).
- ``LIGHT_YELLOW``: (255, 255, 224).
- ``LIGHT_GRAY``: (211, 211, 211).
- ``LIGHT_PINK``: (255, 182, 193).
- ``LIGHT_PURPLE``: (204, 153, 255).
- ``LIGHT_ORANGE``: (255, 200, 120).
- ``LIGHT_BROWN``: (210, 180, 140).
"""

from dataclasses import dataclass
from typing import Self

__all__ = [
    "BEIGE",
    "BLACK",
    "BLUE",
    "BROWN",
    "CORAL",
    "CYAN",
    "GOLD",
    "GRAY",
    "GREEN",
    "INDIGO",
    "LIGHT_BLUE",
    "LIGHT_BROWN",
    "LIGHT_CYAN",
    "LIGHT_GRAY",
    "LIGHT_GREEN",
    "LIGHT_ORANGE",
    "LIGHT_PINK",
    "LIGHT_PURPLE",
    "LIGHT_RED",
    "LIGHT_YELLOW",
    "LIME",
    "MAGENTA",
    "MAROON",
    "NAVY",
    "OLIVE",
    "ORANGE",
    "PINK",
    "PURPLE",
    "RED",
    "SILVER",
    "TEAL",
    "TURQUOISE",
    "VIOLET",
    "WHITE",
    "YELLOW",
    "Color",
]


@dataclass(repr=False)
class Color:
    """
    RGB color container.

    Attributes:
        r: Red channel (0-255).
        g: Green channel (0-255).
        b: Blue channel (0-255).
    """

    r: int
    g: int
    b: int

    def tikz(self) -> str:
        return f"{{rgb,255: red,{self.r}; green,{self.g}; blue,{self.b}}}"

    def svg(self) -> str:
        return f"rgb({self.r}, {self.g}, {self.b})"

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.r + other.r, self.g + other.g, self.b + other.b)

    def __iadd__(self, other: Self) -> Self:
        self.r += other.r
        self.g += other.g
        self.b += other.b
        return self

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.r - other.r, self.g - other.g, self.b - other.b)

    def __isub__(self, other: Self) -> Self:
        self.r -= other.r
        self.g -= other.g
        self.b -= other.b
        return self

    def __mul__(self, alpha: float) -> Self:
        return self.__class__(
            int(self.r * alpha), int(self.g * alpha), int(self.b * alpha)
        )

    def __rmul__(self, alpha: float) -> Self:
        return self * alpha

    def __imul__(self, alpha: float) -> Self:
        self.r = int(self.r * alpha)
        self.g = int(self.g * alpha)
        self.b = int(self.b * alpha)
        return self

    def __truediv__(self, alpha: float) -> Self:
        return self.__class__(
            int(self.r / alpha), int(self.g // alpha), int(self.b / alpha)
        )

    def __itruediv__(self, alpha: float) -> Self:
        self.r = int(self.r / alpha)
        self.g = int(self.g / alpha)
        self.b = int(self.b / alpha)
        return self


BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
LIME = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
YELLOW = Color(255, 255, 0)
CYAN = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)
SILVER = Color(192, 192, 192)
GRAY = Color(128, 128, 128)
MAROON = Color(128, 0, 0)
OLIVE = Color(128, 128, 0)
GREEN = Color(0, 128, 0)
PURPLE = Color(128, 0, 128)
TEAL = Color(0, 128, 128)
NAVY = Color(0, 0, 128)
ORANGE = Color(255, 165, 0)
PINK = Color(255, 192, 203)
BROWN = Color(165, 42, 42)
GOLD = Color(255, 215, 0)
INDIGO = Color(75, 0, 130)
VIOLET = Color(238, 130, 238)
BEIGE = Color(245, 245, 220)
TURQUOISE = Color(64, 224, 208)
CORAL = Color(255, 127, 80)

LIGHT_RED = Color(255, 128, 128)
LIGHT_BLUE = Color(173, 216, 230)
LIGHT_GREEN = Color(144, 238, 144)
LIGHT_CYAN = Color(224, 255, 255)
LIGHT_YELLOW = Color(255, 255, 224)
LIGHT_GRAY = Color(211, 211, 211)
LIGHT_PINK = Color(255, 182, 193)
LIGHT_PURPLE = Color(204, 153, 255)
LIGHT_ORANGE = Color(255, 200, 120)
LIGHT_BROWN = Color(210, 180, 140)
