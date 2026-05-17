from collections.abc import Callable, Iterable
from math import cos, isclose, sin, sqrt
from typing import Any, Self, cast

from .backend import fill_default_args, svg_command, tikz_command
from .circle import Circle, Ellipse
from .curve import Parametric
from .pobject import PObject, POProperty, RenderingContext
from .shape import Path
from .style import CustomStyle, color
from .style.draw import Stroke
from .utils import cartesian_to_canvas
from .vector import Vector

__all__ = [
    "Line",
    "_intersect_line_and_path",
    "_intersect_line_and_segment",
    "_unpack_simple_intersection",
    "intersect_segments",
    "segment_contains",
]


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
        :math:`\ell : ax + by = c.`

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

    def __and__(self, other: Self | Circle | Ellipse | Path | Parametric) -> Any:
        """
        Find the intersection between the line and another figure.

        Raises:
            ValueError: If the right operand is not a :class:`Line` or
                a :class:`Circle <pythagoras.circle.Circle>`.
        """
        if isinstance(other, self.__class__):
            if self.direction | other.direction:
                return (
                    self
                    if self.point == other.point
                    or Vector.from_two_points(self.point, other.point) | self.direction
                    else None
                )
            a1, b1, c1 = self.implicit
            a2, b2, c2 = other.implicit
            d = a1 * b2 - b1 * a2
            return ((c1 * b2 - c2 * b1) / d, (c2 * a1 - c1 * a2) / d)
        if isinstance(other, Circle):
            a, b, c = self.implicit
            c1, c2, r = other.x, other.y, other.radius
            q = 1 + a**2 / b**2
            t = -2 * (c1 + a * c / (b**2) - a * c2 / b)
            s = c1**2 + (c / b - c2) ** 2 - r**2
            delta = t**2 - 4 * q * s
            if isclose(delta, 0, abs_tol=1e-9):
                return (-t / (2 * q), -a * (-t / (2 * q)) / b + c / b)
            elif delta < 0:
                return None
            x1 = (-t + sqrt(delta)) / (2 * q)
            x2 = (-t - sqrt(delta)) / (2 * q)
            return ((x1, -a * x1 / b + c / b), (x2, -a * x2 / b + c / b))
        if isinstance(other, Ellipse):
            dx = self.point[0] - other.x
            dy = self.point[1] - other.y
            s, c = sin(-other.theta), cos(-other.theta)
            x0 = dx * c - dy * s
            y0 = dx * s + dy * c
            vx = self.direction.x * c - self.direction.y * s
            vy = self.direction.x * s + self.direction.y * c
            a = (vx**2) / (other.rx**2) + (vy**2) / (other.ry**2)
            b = 2 * ((x0 * vx) / (other.rx**2) + (y0 * vy) / (other.ry**2))
            c = (x0**2) / (other.rx**2) + (y0**2) / (other.ry**2) - 1
            delta = b**2 - 4 * a * c
            ts: list[float] = []
            if isclose(delta, 0, abs_tol=1e-9):
                ts.append(-b / (2 * a))
            elif delta < 0:
                return None
            elif delta > 0:
                ts.append((-b + sqrt(delta)) / (2 * a))
                ts.append((-b - sqrt(delta)) / (2 * a))
            return tuple(
                (
                    self.point[0] + t * self.direction.x,
                    self.point[1] + t * self.direction.y,
                )
                for t in ts
            )
        if isinstance(other, Path):
            return _intersect_line_and_path(self, other.points)
        if isinstance(other, Parametric):
            return _intersect_line_and_path(self, other.make_points())
        else:
            return NotImplemented

    def __rand__(self, other: Self | Circle | Ellipse | Path | Parametric) -> Any:
        return self & other


def _intersect_line_and_segment(
    line: Line, pa: tuple[float, float], pb: tuple[float, float]
) -> None | tuple[float, float] | tuple[tuple[float, float], tuple[float, float]]:
    """
    Intersects a :class:`Line` object with the segment that joins the two given points.
    This function is not meant to be called by the user, but rather within the :class:`Line`
    and :class:`Triangle <pythagoras.triangle.Triangle>` intersection (&) operators.

    Parameters:
        line: The given line.
        pa: First point of the segment.
        pb: Second point of the segment.

    Returns:
        The intersection of the line with the segment. If two points are returned, it is because
        the intersction is the segment that joins those two; if one point is returned, they intersect
        at a single point; if `None` is returned, the line and the segment do not intersect.
    """
    v = Vector.from_two_points(pb, pa)
    w = Vector.from_two_points(line.point, pa)
    if (d := line.direction ^ v) == 0:
        return (pa, pb) if v | w else None
    u = line.direction ^ w / d
    if u < 0 or u > 1:
        return None
    return (pa[0] - u * v.x, pa[1] - u * v.y)


def _intersect_line_and_path(
    line: Line, ps: list[tuple[float, float]]
) -> None | list[tuple[float, float] | tuple[tuple[float, float], tuple[float, float]]]:
    """
    Intersects a :class:`Line` object with a path described by the endpoints of its segments.
    This function is not meant to be called by the user, but rather within the :class:`Line`
    and :class:`Triangle <pythagoras.triangle.Triangle>` intersection (&) operators.

    Parameters:
        line: The given line.
        ps: Endpoints of the segments.

    Returns:
        A list with either points or segments in the format described in :meth:`_intersect_line_and_segment`,
        or `None` if there is no intersection whatsoever.
    """
    cap: list[Any] = []
    for i in range(len(ps) - 1):
        if x := _intersect_line_and_segment(line, ps[i], ps[i + 1]):
            cap.append(x)
    return cap if len(cap) else None


def _unpack_simple_intersection(
    i: None | tuple[float, float] | Iterable[tuple[float, float]],
    a: tuple[float, float] | None = None,
    b: tuple[float, float] | None = None,
) -> list[tuple[float, float]]:
    r"""
    Given an intersection of at most two points, it returns it as a list of its points. If `a`
    and `b` are not `None`, it filters those that lie within the segment :math:`\overline{\rm AB}.`
    This function is not meant to be called by the user, but rather within the :class:`Line`
    and :class:`Triangle <pythagoras.triangle.Triangle>` intersection (&) operators.

    Parameters:
        i: Intersection of figures, given as either `None`, a point, or an iterable of points.
        a: First endpoint of the segment if specified.
        b: Second endpoint of the segment if specified.

    Returns:
        Filtered points of the intersection.
    """
    sc: Callable[
        [tuple[float, float], tuple[float, float] | None, tuple[float, float] | None],
        bool,
    ] = (
        (
            lambda _i, _a, _b: segment_contains(
                _i, cast(tuple[float, float], _a), cast(tuple[float, float], _b)
            )
        )
        if a and b
        else lambda _, __, ___: True
    )
    if not i:
        return []
    if isinstance(i, tuple) and isinstance(i[0], float):
        i = cast(tuple[float, float], i)
        return [i] if sc(i, a, b) else []
    i = cast(Iterable[tuple[float, float]], i)
    return [j for j in i if sc(j, a, b)]


def segment_contains(
    p: tuple[float, float], pa: tuple[float, float], pb: tuple[float, float]
) -> bool:
    r"""
    Checks whether a point lies in the segment that joins :math:`\rm A` and :math:`\rm B`.

    Parameters:
        p: Point to analyze.
        pa: First endpoint of the segment.
        pb: Second endpoint of the segment.

    Returns:
        Whether :math:`\rm P \in \overline{AB}`.
    """
    u = Vector.from_two_points(pa, pb)
    v = Vector.from_two_points(pa, p)
    d = u @ v
    if not isclose(u ^ v, 0, abs_tol=1e-9) or d < -1e-9:
        return False
    return d <= abs(u) ** 2


def intersect_segments(
    a1: tuple[float, float],
    b1: tuple[float, float],
    a2: tuple[float, float],
    b2: tuple[float, float],
) -> None | tuple[float, float] | tuple[tuple[float, float], tuple[float, float]]:
    """
    Computes the intersection between two segments, described by their endpoints.

    Parameters:
        a1: First endpoint of the first segment.
        b1: Second endpoint of the first segment.
        a2: First endpoint of the second segment.
        b2: Second endpoint of the second segment.

    Returns:
        `None` if the two segments do not intersect, two delimiting points if they
        intersect at another segment, or a point otherwise.
    """
    l = Line.from_two_points(a1, b1)
    i = _intersect_line_and_segment(l, a2, b2)
    if not i:
        return None
    if isinstance(i[0], float):
        i = cast(tuple[float, float], i)
        return i if segment_contains(i, a1, b1) else None
    (a1, b1), (a2, b2) = sorted((a1, b1)), sorted((a2, b2))
    return (i, e) if (i := max(a1, a2)) <= (e := min(b1, b2)) else None
