from dataclasses import dataclass

from .pobject import PObject, POProperty

__all__ = ["Phantom", "cartesian_to_canvas"]


def cartesian_to_canvas(
    x: float, y: float, width: float, height: float, scale: float
) -> tuple[float, float]:
    return (width / 2 + x * scale, height / 2 - y * scale)


@dataclass
class Phantom(PObject):
    """
    A zero-size placeholder element used for layout or reference.

    Attributes:
        x: :math:`x`-coordinate in Cartesian space.
        y: :math:`y`-coordinate in Cartesian space.
    """

    x: float
    y: float

    def extrema(self) -> list[tuple[float, float]]:
        return [(self.x, self.y)]

    def tikz(self, *args: POProperty) -> str:
        return f"% Phantom element at ({self.x}, {self.y})"

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: POProperty,
    ) -> str:
        return f"<!-- Phantom element at ({self.x}, {self.y} --"
