from collections.abc import Iterator
from math import cos, floor, inf, radians, sin, sqrt, tau
from typing import Self

from .backend import fill_default_args, svg_path, tikz_command
from .pobject import PObject, POProperty, RenderingContext
from .style import color
from .style.draw import Fill, Stroke
from .utils import cartesian_to_canvas

__all__ = ["Path", "Polygon", "grid"]


class Path(PObject):
    """
    A sequence of connected points forming an open path.

    Attributes:
        *args: Points specified as `(x, y)` pairs defining the path.
        zord: Drawing order; higher values are drawn later.
    """

    points: list[tuple[float, float]]

    def __init__(self, *args: tuple[float, float], zord: int = 0) -> None:
        self.points = list(args)
        self._zord = zord
        if len(self.points) < 2:
            raise RuntimeError("A path must have at least two points.")

    def extrema(self) -> list[tuple[float, float]]:
        mxx, mxy, mnx, mny = -inf, -inf, inf, inf
        for p in self.points:
            if p[0] < mnx:
                mnx = p[0]
            if p[0] > mxx:
                mxx = p[0]
            if p[1] < mny:
                mny = p[1]
            if p[1] > mxy:
                mxy = p[1]
        return [(mnx, mny), (mxx, mxy)]

    def tikz(self, ctx: RenderingContext, *args: POProperty) -> str:
        return tikz_command(
            "draw", " -- ".join(f"({p[0]}, {p[1]})" for p in self.points), *args
        )

    def svg(self, ctx: RenderingContext, *args: POProperty) -> str:
        return svg_path(
            (cartesian_to_canvas(p, ctx) for p in self.points),
            *fill_default_args(args, (Fill, Fill(None)), (Stroke, Stroke(color.BLACK))),
        )

    def rotate(self, point: tuple[float, float], theta: float) -> None:
        """
        Rotates all the points of the `Shape` object by a given angle around some point,
        and consequently the shape itself.

        Parameters:
            point: Center of rotation.
            theta: Angle of rotation.
        """
        px, py = point
        alpha = radians(theta)
        self.points = [
            (
                (x - px) * cos(alpha) - (y - py) * sin(alpha) + py,
                (x - px) * sin(alpha) + (y - py) * cos(alpha),
            )
            for x, y in self.points
        ]


class Polygon(Path):
    """
    A closed polygonal shape.

    Notes:
        The polygon is drawn by connecting the provided points and closing
        the path (the first point is repeated for SVG output).
    """

    def tikz(self, ctx: RenderingContext, *args: POProperty) -> str:
        return tikz_command(
            "draw",
            " -- ".join(f"({p[0]}, {p[1]})" for p in self.points) + " -- cycle",
            *args,
        )

    def svg(self, ctx: RenderingContext, *args: POProperty) -> str:
        self.points.append(self.points[0])
        code = super().svg(ctx, *args)
        self.points.pop()
        return code

    @classmethod
    def regular(cls, x: float, y: float, r: float, n: int, zord: int = 0) -> Self:
        """
        Constructor for a regular polygon.

        Parameters:
            x: :math:`x`-coordinate of the center.
            y: :math:`y`-coordinate of the center.
            r: Radius of the polygon (distance from the center to a vertex).
            n: Number of sides.
            zord: Rendering priority.

        Returns:
            An instance of the `Polygon` class.
        """
        ps = ((x + r * cos(i * tau / n), y + r * sin(i * tau / n)) for i in range(n))
        return cls(*ps, zord=zord)

    @classmethod
    def triangle_from_lengths(cls, a: float, b: float, c: float, zord: int = 0) -> Self:
        """
        Construct a triangle from the lengths of its sides.

        Parameters:
            a: Length of the first side.
            b: Length of the second side.
            c: Length of the third side.

        Returns:
            An instance of the `Polygon` class.
        """
        a, b, c = sorted([a, b, c])
        if a + b <= c:
            raise ValueError("The given lengths cannot form a valid triangle.")
        x = (c**2 + b**2 - a**2) / (2 * c)
        y = sqrt(abs(b**2 - x**2))
        cx = (0 + c + x) / 3
        cy = y / 3
        return cls((-cx, -cy), (c - cx, -cy), (x - cx, y - cy), zord=zord)


def grid(
    start: tuple[float, float],
    end: tuple[float, float],
    step: tuple[float, float],
    zord: int = 0,
) -> Iterator[Path]:
    """
    Creates a sequence of segments forming a grid.

    Parameters:
        start: Leftmost bottom point of the grid.
        end: Rightmost top point of the grid.
        step: Increments in the :math:`x` and :math:`y` axes.

    Returns:
        An iterable of lines shaping a grid.
    """
    px = start[0] + floor((end[0] - start[0]) / step[0]) * step[0]
    py = start[1] + floor((end[1] - start[1]) / step[1]) * step[1]
    y = start[1]
    while y <= end[1]:
        yield Path((start[0], y), (px, y), zord=zord)
        y += step[1]
    x = start[0]
    while x <= end[0]:
        yield Path((x, start[1]), (x, py), zord=zord)
        x += step[0]
