from dataclasses import dataclass
from math import isclose

from .pobject import PObject, POProperty, RenderingContext
from .vector import Vector

__all__ = ["Phantom", "cartesian_to_canvas", "intersect_segments", "segment_contains"]


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

    Raises:
        ValueError: If one of the two segments is degenerate, i.e., its delimiting
        points are the same.
    """
    u, v = Vector.from_two_points(a1, b1), Vector.from_two_points(a2, b2)
    if u() == (0, 0):
        raise ValueError("The first segment must have a nonzero length")
    if v() == (0, 0):
        raise ValueError("The second segment must have a nonzero length")

    w = Vector.from_two_points(a1, a2)
    if u | v:
        if a1 != a2 and not w | u:
            return None
        (a1, b1), (a2, b2) = sorted((a1, b1)), sorted((a2, b2))
        return (i, e) if (i := max(a1, a2)) <= (e := min(b1, b2)) else None

    d = u ^ v
    k = u ^ w / d
    t = v ^ w / d
    if (k < -1 or k > 0) or (t < -1 or t > 0):
        return None

    return (a2[0] - k * v.x, a2[1] - k * v.y)


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
