from dataclasses import dataclass

from .pobject import PObject, POProperty, RenderingContext

__all__ = ["Phantom", "cartesian_to_canvas"]


def cartesian_to_canvas(
    p: tuple[float, float], ctx: RenderingContext
) -> tuple[float, float]:
    """
    Converts a point in Cartesian coordinates into the canvas coordinate system.

    Parameters:
        p: Point to be converted.
        ctx: Properties associated to the canvas.

    Returns:
        The point in canvas coordinates.
    """
    origin = ctx.origin
    return (
        ctx.width / 2 + (p[0] - origin[0]) * ctx.scale,
        ctx.height / 2 - (p[1] - origin[1]) * ctx.scale,
    )


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

    def tikz(self, ctx: RenderingContext, *args: POProperty) -> str:
        return f"% Phantom element at ({self.x}, {self.y})"

    def svg(self, ctx: RenderingContext, *args: POProperty) -> str:
        return f"<!-- Phantom element at ({self.x}, {self.y} -->"
