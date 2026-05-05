from typing import Self

from .backend import fill_default_args, svg_command, tikz_command
from .pobject import PObject, POProperty, RenderingContext
from .style import CustomStyle, color
from .style.draw import Stroke
from .utils import cartesian_to_canvas
from .vector import Vector


class Line(PObject):
    r"""
    Line in :math:`\mathbf R^2`. Contrary to a :class:`Path <pythagoras.shape.Path>` object,
    a line extends throughout the entirety of the canvas.

    Attributes:
        point: A point that belongs to the line.
        direction: Direction vector.
    """

    point: tuple[float, float]
    direction: Vector

    def __init__(
        self, point: tuple[float, float], direction: Vector, zord: int = 0
    ) -> None:
        self.point = point
        self.direction = direction
        self._zord = zord

    @classmethod
    def from_two_points(
        cls, p1: tuple[float, float], p2: tuple[float, float], zord: int = 0
    ) -> Self:
        """
        Constructs the unique line that passes through two points.

        Parameters:
            p1: First point.
            p2: Second point.

        Returns:
            A line that contains `p1` and `p2`.
        """
        return cls(p1, Vector.from_two_points(p1, p2), zord)

    @classmethod
    def from_implicit(cls, a: float, b: float, c: float, zord: int = 0) -> Self:
        r"""
        Creates a line from its implicit equation, where it is given as
        ..math::

            \ell : ax + by = c.

        Returns:
            The line with that implicit equation.

        Raises:
            ValueError: If both a and b are zero.
        """
        if a == b == 0:
            raise ValueError("Both a and b cannot be zero at the same time.")
        if b == 0:
            return cls((c / a, 0), Vector(0, 1), zord)
        return cls((0, c / b), Vector(b, -a))

    @property
    def implicit(self) -> tuple[float, float, float]:
        """
        Gives the line expressed in an implicit equation, where the numbers
        are the coefficients of :math:`x` and :math:`y`, and the independent term
        (see :meth:`from_implicit`).
        """
        return (
            self.direction.y,
            -self.direction.x,
            self.direction.y * self.point[0] - self.direction.x * self.point[1],
        )

    def _make_bounding_points(
        self, ctx: RenderingContext
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        if self.direction.x == 0:
            return ((self.point[0], ctx.ymax), (self.point[0], ctx.ymin))
        if self.direction.y == 0:
            return ((ctx.xmin, self.point[1]), (ctx.xmax, self.point[1]))
        a, b, c = self.implicit
        ps = [
            (ctx.xmax, c / b - a / b * ctx.xmax),
            (ctx.xmin, c / b - a / b * ctx.xmin),
            (c / a - b / a * ctx.ymax, ctx.ymax),
            (c / a - b / a * ctx.ymin, ctx.ymin),
        ]
        ps = [
            (x, y)
            for x, y in ps
            if ctx.xmin <= x <= ctx.xmax and ctx.ymin <= y <= ctx.ymax
        ]
        return (ps[0], ps[1])

    def extrema(self) -> list[tuple[float, float]]:
        return []

    def svg(self, ctx: RenderingContext, *args: POProperty) -> str:
        (x1, y1), (x2, y2) = (
            cartesian_to_canvas(p, ctx) for p in self._make_bounding_points(ctx)
        )
        return svg_command(
            "line",
            CustomStyle("x1", x1),
            CustomStyle("y1", y1),
            CustomStyle("x2", x2),
            CustomStyle("y2", y2),
            *fill_default_args(args, (Stroke, Stroke(color.BLACK))),
        )

    def tikz(self, ctx: RenderingContext, *args: POProperty) -> str:
        p1, p2 = self._make_bounding_points(ctx)
        return tikz_command("draw", f"{p1} -- {p2}", *args)

    def __contains__(self, point: tuple[float, float]) -> bool:
        """
        Checks whether a point belongs to the line.

        Returns:
            `True` if its lies on the line, `False` otherwise.
        """
        a, b, c = self.implicit
        return a * point[0] + b * point[1] == c
