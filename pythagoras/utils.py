from dataclasses import dataclass

from .pobject import PObject, POProperty

__all__ = ["Phantom", "cartesian_to_canvas"]


def cartesian_to_canvas(
    x: float,
    y: float,
    width: float,
    height: float,
    scale: float,
    origin: tuple[float, float],
) -> tuple[float, float]:
    """
    Converts a point in Cartesian coordinates into the canvas coordinate system.

    Parameters:
        x: :math:`x`-coordinate of the point.
        y: :math:`y`-coordinate of the point.
        width: Width of the canvas.
        height: Height of the canvas.
        scale: Scaling factor of the canvas.
        origin: Center of the figure in canvas coordinates.

    Returns:
        The point in canvas coordinates.
    """
    return (width / 2 + x * scale - origin[0], height / 2 - y * scale + origin[1])


@dataclass(init=False)
class Phantom(PObject):
    """
    A zero-size placeholder element used for layout or reference.

    Attributes:
        x: :math:`x`-coordinate in Cartesian space.
        y: :math:`y`-coordinate in Cartesian space.
    """

    x: float
    y: float

    def __init__(self, x: float, y: float, zord: int = 0) -> None:
        self.x = x
        self.y = y
        self._zord = zord

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
        return f"<!-- Phantom element at ({self.x}, {self.y} -->"
