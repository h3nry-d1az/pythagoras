from collections.abc import Callable
from itertools import combinations
from math import acos, cos, pi, sin, sqrt, tan
from typing import Annotated, Any, Self, cast

from ..backend import fill_default_args, svg_path, tikz_command
from ..circle import Circle, Ellipse
from ..curve import Parametric
from ..line import (
    Line,
    _intersect_line_and_path,  # pyright: ignore[reportPrivateUsage]
    _unpack_simple_intersection,  # pyright: ignore[reportPrivateUsage]
    intersect_segments,
)
from ..pobject import PObject, POProperty, RenderingContext
from ..shape import Path
from ..style.color import BLACK
from ..style.draw import Fill, Stroke
from ..utils import cartesian_to_canvas
from ..vector import Vector, dist

__all__ = ["GenericBarycentric", "GenericCartesian", "GenericTrilinear", "Triangle"]


class Triangle(PObject):
    r"""
    Triangle described by three points in :math:`\mathbf R^2`.
    """

    __pa: tuple[float, float]
    __pa: tuple[float, float]
    __pa: tuple[float, float]
    __a: float
    __b: float
    __c: float
    __alpha: float
    __beta: float
    __gamma: float

    def _fill_data(self) -> None:
        """
        Completes the sidelengths and angles of the triangle given its three describing
        points.
        """
        AB = Vector.from_two_points(self.__pa, self.__pb)
        BC = Vector.from_two_points(self.__pb, self.__pc)
        CA = Vector.from_two_points(self.__pc, self.__pa)
        self.__a = abs(BC)
        self.__b = abs(CA)
        self.__c = abs(AB)
        self.__alpha = acos((AB @ -CA) / (abs(AB) * abs(CA)))
        self.__beta = acos(((-AB) @ BC) / (abs(AB) * abs(BC)))
        self.__gamma = acos((CA @ (-BC)) / (abs(CA) * abs(BC)))

    def __init__(
        self,
        A: tuple[float, float],
        B: tuple[float, float],
        C: tuple[float, float],
        zord: int = 0,
    ) -> None:
        self.__pa = A
        self.__pb = B
        self.__pc = C
        self._fill_data()
        self._zord = zord

    @classmethod
    def from_lengths(
        cls,
        a: float,
        b: float,
        c: float,
        centroid: tuple[float, float] = (0, 0),
        zord: int = 0,
    ) -> Self:
        """
        Construct a triangle from the lengths of its sides.

        Parameters:
            a: Length of the first side.
            b: Length of the second side.
            c: Length of the third side.
            centroid: Centroid of the triangle; by default is the origin.

        Returns:
            Triangle with sides measuring `a`, `b`, and `c`.
        """
        a, b, c = sorted([a, b, c])
        if a + b <= c:
            raise ValueError("The lengths cannot form a valid triangle.")
        x = (c**2 + b**2 - a**2) / (2 * c)
        y = sqrt(abs(b**2 - x**2))
        cx = (0 + c + x) / 3
        cy = y / 3
        return cls(
            (-cx + centroid[0], -cy + centroid[1]),
            (c - cx + centroid[0], -cy + centroid[1]),
            (x - cx + centroid[0], y - cy + centroid[1]),
            zord=zord,
        )

    def incircle(
        self,
    ) -> tuple[Circle, tuple[float, float], tuple[float, float], tuple[float, float]]:
        """
        Gives the incircle of the triangle together with its tangency points.
        Wrapper for :meth:`pythagoras.circle.Circle.triangle_incircle`.
        """
        return Circle.triangle_incircle(self.A, self.B, self.C, self._zord)

    def excircle_A(
        self,
    ) -> tuple[Circle, tuple[float, float], tuple[float, float], tuple[float, float]]:
        r"""Gives the :math:`\rm A`-excircle of the triangle together with its tangency points."""
        s = self.s
        return (
            Circle(*self.excenter_A, self.exradius_A, self._zord),
            self.barycentric((0, s - self.b, s - self.c)),
            self.barycentric((self.c - s, s, 0)),
            self.barycentric((self.b - s, 0, s)),
        )

    def excircle_B(
        self,
    ) -> tuple[Circle, tuple[float, float], tuple[float, float], tuple[float, float]]:
        r"""Gives the :math:`\rm B`-excircle of the triangle together with its tangency points."""
        s = self.s
        return (
            Circle(*self.excenter_B, self.exradius_B, self._zord),
            self.barycentric((s - self.a, 0, s - self.c)),
            self.barycentric((0, self.a - s, s)),
            self.barycentric((s, self.c - s, 0)),
        )

    def excircle_C(
        self,
    ) -> tuple[Circle, tuple[float, float], tuple[float, float], tuple[float, float]]:
        r"""Gives the :math:`\rm C`-excircle of the triangle together with its tangency points."""
        s = self.s
        return (
            Circle(*self.excenter_C, self.exradius_C, self._zord),
            self.barycentric((s - self.a, s - self.b, 0)),
            self.barycentric((0, s, self.a - s)),
            self.barycentric((s, 0, self.b - s)),
        )

    def circumcircle(self) -> Circle:
        """
        Produces the circumcircle of the triangle.
        Wrapper for :meth:`pythagoras.circle.Circle.triangle_circumcircle`.
        """
        return Circle.triangle_circumcircle(self.A, self.B, self.C, self._zord)

    def nine_point_circle(self) -> Circle:
        """Constructs the nine-point circle of the triangle."""
        return Circle(*self.npcenter, self.npradius, zord=self._zord)

    @property
    def A(self) -> tuple[float, float]:
        r"""First of the points of the triangle; denoted by :math:`\rm A`."""
        return self.__pa

    @property
    def B(self) -> tuple[float, float]:
        r"""Second of the points of the triangle; denoted by :math:`\rm B`."""
        return self.__pb

    @property
    def C(self) -> tuple[float, float]:
        r"""Third of the points of the triangle; denoted by :math:`\rm C`."""
        return self.__pc

    @A.setter
    def A(self, pa: tuple[float, float]) -> None:
        self.__pa = pa
        self._fill_data()

    @B.setter
    def B(self, pb: tuple[float, float]) -> None:
        self.__pb = pb
        self._fill_data()

    @C.setter
    def C(self, pc: tuple[float, float]) -> None:
        self.__pc = pc
        self._fill_data()

    @property
    def a(self) -> float:
        r"""Length of the side opposite to :math:`\rm A`."""
        return self.__a

    @property
    def b(self) -> float:
        r"""Length of the side opposite to :math:`\rm B`."""
        return self.__b

    @property
    def c(self) -> float:
        r"""Length of the side opposite to :math:`\rm C`."""
        return self.__c

    @property
    def s(self) -> float:
        r"""Semiperimeter of the triangle."""
        return (self.a + self.b + self.c) / 2

    @property
    def alpha(self) -> float:
        r"""
        Angle that corresponds to the vertex :math:`\rm A`, i.e.,
        :math:`\alpha = \min\{\angle BAC, \angle CAB\}.`
        """
        return self.__alpha

    @property
    def beta(self) -> float:
        r"""
        Angle that corresponds to the vertex :math:`\rm B`, i.e.,
        :math:`\beta = \min\{\rm \angle ABC, \angle CBA\}.`
        """
        return self.__beta

    @property
    def gamma(self) -> float:
        r"""
        Angle that corresponds to the vertex :math:`\rm C`, i.e.,
        :math:`\alpha = \min\{\rm \angle ACB, \angle BCA\}.`
        """
        return self.__gamma

    def extrema(self) -> list[tuple[float, float]]:
        return [self.A, self.B, self.C]

    def tikz(self, ctx: RenderingContext, *args: POProperty) -> str:
        return tikz_command("draw", f"{self.A} -- {self.B} -- {self.C} -- cycle", *args)

    def svg(self, ctx: RenderingContext, *args: POProperty) -> str:
        pa, pb, pc = (cartesian_to_canvas(p, ctx) for p in (self.A, self.B, self.C))
        return svg_path(
            (pa, pb, pc, pa),
            *fill_default_args(args, (Fill, Fill(None)), (Stroke, Stroke(BLACK))),
        )

    def translate(self, vector: Vector) -> None:
        r"""
        Moves all the vertices of the triangle (and thus the triangle itself) along a vector.

        Parameters:
            vector: Translation vector to apply to :math:`\rm A, B, C`.
        """
        self.__pa = (self.__pa[0] + vector.x, self.__pa[1] + vector.y)
        self.__pb = (self.__pb[0] + vector.x, self.__pb[1] + vector.y)
        self.__pc = (self.__pc[0] + vector.x, self.__pc[1] + vector.y)

    def translated(self, vector: Vector, zord: int = 0) -> Self:
        r"""
        Produces a copy of the triangle translated along the given vector.

        Parameters:
            vector: Translation vector to apply to :math:`\rm A, B, C`.
            zord: Rendering priority of the new instance.

        Returns:
            The new, translated triangle.
        """
        return self.__class__(
            (self.__pa[0] + vector.x, self.__pa[1] + vector.y),
            (self.__pb[0] + vector.x, self.__pb[1] + vector.y),
            (self.__pc[0] + vector.x, self.__pc[1] + vector.y),
            zord=zord,
        )

    def rotate(self, point: tuple[float, float], theta: float) -> None:
        r"""
        Rotates the triangle around the given point by an angle :math:`\theta`.

        Parameters:
            point: Point of rotation.
            theta: Angle of rotation.
        """
        xa, ya = self.__pa
        xb, yb = self.__pb
        xc, yc = self.__pc
        xp, yp = point
        self.__pa = (
            (xa - xp) * cos(theta) - (ya - yp) * sin(theta) + yp,
            (xa - xp) * sin(theta) + (ya - yp) * cos(theta),
        )
        self.__pb = (
            (xb - xp) * cos(theta) - (yb - yp) * sin(theta) + yp,
            (xb - xp) * sin(theta) + (yb - yp) * cos(theta),
        )
        self.__pc = (
            (xc - xp) * cos(theta) - (yc - yp) * sin(theta) + yp,
            (xc - xp) * sin(theta) + (yc - yp) * cos(theta),
        )

    def rotated(self, point: tuple[float, float], theta: float, zord: int = 0) -> Self:
        r"""
        Produces a copy of the triangle rotated around the given point by an angle :math:`\theta`.

        Parameters:
            point: Point of rotation.
            theta: Angle of rotation.
            zord: Rendering priority of the new instance.

        Returns:
            The new, rotated triangle.
        """
        xa, ya = self.__pa
        xb, yb = self.__pb
        xc, yc = self.__pc
        xp, yp = point
        return self.__class__(
            (
                (xa - xp) * cos(theta) - (ya - yp) * sin(theta) + yp,
                (xa - xp) * sin(theta) + (ya - yp) * cos(theta),
            ),
            (
                (xb - xp) * cos(theta) - (yb - yp) * sin(theta) + yp,
                (xb - xp) * sin(theta) + (yb - yp) * cos(theta),
            ),
            (
                (xc - xp) * cos(theta) - (yc - yp) * sin(theta) + yp,
                (xc - xp) * sin(theta) + (yc - yp) * cos(theta),
            ),
            zord=zord,
        )

    def __add__(self, vector: Vector) -> Self:
        return self.translated(vector)

    def __iadd__(self, vector: Vector) -> Self:
        self.translate(vector)
        return self

    def __abs__(self) -> float:
        """Computes the area of the triangle."""
        xa, ya = self.__pa
        xb, yb = self.__pb
        xc, yc = self.__pc
        return (xa * (yb - yc) + xb * (yc - ya) + xc * (ya - yb)) / 2

    def barycentric(self, coords: tuple[float, float, float]) -> tuple[float, float]:
        """
        Converts a point from barycentric to Cartesian coordinates.

        Parameters:
            coords: Barycentric coordinates of the point.

        Returns:
            The point expressed in the Cartesian plane.
        """
        n = sum(coords)
        u, v, w = (coords[0] / n, coords[1] / n, coords[2] / n)
        return (
            u * self.__pa[0] + v * self.__pb[0] + w * self.__pc[0],
            u * self.__pa[1] + v * self.__pb[1] + w * self.__pc[1],
        )

    def to_barycentric(self, coords: tuple[float, float]) -> tuple[float, float, float]:
        """
        Computes the (normalized) barycentric coordinates of a point in the Cartesian plane.

        Parameters:
            coords: Point in Cartesian coordinates.

        Returns:
            The point expressed in normalized barycentric coordinates.
        """
        xa, ya = self.__pa
        xb, yb = self.__pb
        xc, yc = self.__pc
        xp, yp = coords
        d = (yb - yc) * (xa - xc) + (xc - xb) * (ya - yc)
        u = ((yb - yc) * (xp - xc) + (xc - xb) * (yp - yc)) / d
        v = ((yc - ya) * (xp - xc) + (xa - xc) * (yp - yc)) / d
        return (u, v, 1 - u - v)

    def trilinear(self, coords: tuple[float, float, float]) -> tuple[float, float]:
        """
        Converts a point from trilinear to Cartesian coordinates.

        Parameters:
            coords: Trilinear coordinates of the point.

        Returns:
            The point expressed in the Cartesian plane.
        """
        return self.barycentric(
            (self.a * coords[0], self.b * coords[1], self.c * coords[2])
        )

    def to_trilinear(self, coords: tuple[float, float]) -> tuple[float, float, float]:
        """
        Computes the (normalized) trilinear coordinates of a point in the Cartesian plane.

        Parameters:
            coords: Point in Cartesian coordinates.

        Returns:
            The point expressed in normalized trilinear coordinates.
        """
        u, v, w = self.to_barycentric(coords)
        area = 2 * abs(self)
        return (area * u / self.a, area * v / self.b, area * w / self.c)

    def tripolar(self, coords: tuple[float, float, float]) -> tuple[float, float]:
        """
        Converts a point from tripolar to Cartesian coordinates.

        Parameters:
            coords: Tripolar coordinates of the point.

        Returns:
            The point expressed in the Cartesian plane.
        """
        da, db, dc = coords
        xa, ya = self.__pa
        xb, yb = self.__pb
        xc, yc = self.__pc
        Ra = da**2 - xa**2 - ya**2
        Rb = db**2 - xb**2 - yb**2
        Rc = dc**2 - xc**2 - yc**2
        return (
            ((Ra - Rb) * (yc - yb) - (Rb - Rc) * (yb - ya))
            / (2 * ((xb - xa) * (yc - yb) - (xc - xb) * (yb - ya))),
            ((xb - xa) * (Rb - Rc) - (xc - xb) * (Ra - Rb))
            / (2 * ((xb - xa) * (yc - yb) - (xc - xb) * (yb - ya))),
        )

    def to_tripolar(self, coords: tuple[float, float]) -> tuple[float, float, float]:
        """
        Computes the tripolar coordinates of a point in the Cartesian plane.

        Parameters:
            coords: Point in Cartesian coordinates.

        Returns:
            The point expressed in tripolar coordinates.
        """
        return (
            dist(self.__pa, coords),
            dist(self.__pb, coords),
            dist(self.__pc, coords),
        )

    def contains(self, point: tuple[float, float]) -> bool:
        """Checks whether the given point is inside the triangle."""
        return all(xi >= 0 for xi in self.to_barycentric(point))

    def __contains__(self, point: tuple[float, float]) -> bool:
        return self.contains(point)

    def isogonal_conjugate(self, point: tuple[float, float]) -> tuple[float, float]:
        """
        Calculates the isogonal conjugate of a point expressed in Cartesian coordinates.

        Parameters:
            point: The point in Cartesian coordinates.

        Returns:
            The isogonal conjugate of `point`.
        """
        u, v, w = self.to_barycentric(point)
        return self.barycentric((self.a**2 / u, self.b**2 / v, self.c**2 / w))

    def isotomic_conjugate(self, point: tuple[float, float]) -> tuple[float, float]:
        """
        Calculates the isotomic conjugate of a point expressed in Cartesian coordinates.

        Parameters:
            point: The point in Cartesian coordinates.

        Returns:
            The isotomic conjugate of `point`.
        """
        u, v, w = self.to_barycentric(point)
        return self.barycentric((1 / u, 1 / v, 1 / w))

    def homothety(
        self, point: tuple[float, float], ratio: float, zord: int = 0
    ) -> Self:
        r"""
        Constructs the triangle homothetic to :math:`\triangle \rm ABC` with respect to
        a given point and ratio.

        Parameters:
            point: Center of the homothety.
            ratio: Ratio of the homothety.
            zord: Rendering priority of the new triangle.

        Returns:
            Triangle homothetic to :math:`\triangle \rm ABC`.
        """
        xa, ya = self.__pa
        xb, yb = self.__pb
        xc, yc = self.__pc
        xp, yp = point
        return self.__class__(
            (xp + ratio * (xa - xp), yp + ratio * (ya - yp)),
            (xp + ratio * (xb - xp), yp + ratio * (yb - yp)),
            (xp + ratio * (xc - xp), yp + ratio * (yc - yp)),
            zord=zord,
        )

    @property
    def incenter(self) -> tuple[float, float]:
        """Incenter of the triangle (:math:`X_1`)."""
        return self.barycentric((self.a, self.b, self.c))

    @property
    def inradius(self) -> float:
        """Inradius of the triangle."""
        return 2 * abs(self) / (self.a + self.b + self.c)

    @property
    def excenter_A(self) -> tuple[float, float]:
        r""":math:`\rm A`-excenter of the triangle."""
        return self.barycentric((-self.a, self.b, self.c))

    @property
    def exradius_A(self) -> float:
        r"""Radius of the :math:`\rm A`-excircle."""
        R = self.circumradius
        return 4 * R * sin(self.alpha / 2) * cos(self.beta / 2) * cos(self.gamma / 2)

    @property
    def excenter_B(self) -> tuple[float, float]:
        r""":math:`\rm B`-excenter of the triangle."""
        return self.barycentric((self.a, -self.b, self.c))

    @property
    def exradius_B(self) -> float:
        r"""Radius of the :math:`\rm B`-excircle."""
        R = self.circumradius
        return 4 * R * cos(self.alpha / 2) * sin(self.beta / 2) * cos(self.gamma / 2)

    @property
    def excenter_C(self) -> tuple[float, float]:
        r""":math:`\rm C`-excenter of the triangle."""
        return self.barycentric((self.a, self.b, -self.c))

    @property
    def exradius_C(self) -> float:
        r"""Radius of the :math:`\rm C`-excircle."""
        R = self.circumradius
        return 4 * R * cos(self.alpha / 2) * cos(self.beta / 2) * sin(self.gamma / 2)

    @property
    def centroid(self) -> tuple[float, float]:
        """Centroid of the triangle (:math:`X_2`)."""
        return (
            (self.__pa[0] + self.__pb[0] + self.__pc[0]) / 3,
            (self.__pa[1] + self.__pb[1] + self.__pc[1]) / 3,
        )

    @property
    def circumcenter(self) -> tuple[float, float]:
        """Circumcenter of the triangle (:math:`X_3`)."""
        return self.barycentric(
            (sin(2 * self.alpha), sin(2 * self.beta), sin(2 * self.gamma))
        )

    @property
    def circumradius(self) -> float:
        """Radius of the circumcircle fo the triangle."""
        return self.a / (2 * sin(self.alpha))

    @property
    def orthocenter(self) -> tuple[float, float]:
        """Orthocenter of the triangle (:math:`X_4`)."""
        return self.barycentric((tan(self.alpha), tan(self.beta), tan(self.gamma)))

    @property
    def npcenter(self) -> tuple[float, float]:
        """Center of the nine-point circle of the triangle (:math:`X_5`)."""
        return self.barycentric(
            (
                self.a * cos(self.beta - self.gamma),
                self.b * cos(self.gamma - self.alpha),
                self.c * cos(self.alpha - self.beta),
            )
        )

    @property
    def npradius(self) -> float:
        """
        Radius of the nine-point circle of the triangle.
        It is exactly half the radius of the circumcircle.
        """
        return self.circumradius / 2

    @property
    def lemoine(self) -> tuple[float, float]:
        """Symmedian/Lemoine point of the triangle (:math:`X_6`)."""
        return self.barycentric((self.a**2, self.b**2, self.c**2))

    @property
    def fermat(self) -> tuple[float, float]:
        r"""
        Fermat-Torricelli point of the triangle; coincides with :math:`X_{13}` if no
        angle is greater than :math:`120^\circ`, otherwise it is the vertex of the
        obtuse angle.
        """
        if self.alpha > 2 * pi / 3:
            return self.A
        if self.beta > 2 * pi / 3:
            return self.B
        if self.gamma > 2 * pi / 3:
            return self.C
        return self.barycentric(
            (
                self.a / sin(self.alpha + pi / 3),
                self.b / sin(self.beta + pi / 3),
                self.c / sin(self.gamma + pi / 3),
            )
        )

    def pedal_triangle(self, point: tuple[float, float], zord: int = 0) -> Self:
        """
        Constructs the pedal triangle associated with a given point.

        Parameters:
            point: Point of the pedal triangle.
            zord: Rendering priority of the new shape.

        Returns:
            Pedal triangle associated with `point`.
        """
        ap = Vector.from_two_points(self.__pa, point)
        bp = Vector.from_two_points(self.__pb, point)
        cp = Vector.from_two_points(self.__pc, point)
        ab = Vector.from_two_points(self.__pa, self.__pb)
        bc = Vector.from_two_points(self.__pb, self.__pc)
        ca = Vector.from_two_points(self.__pc, self.__pa)
        p1 = ((ab @ ap / (abs(ab) ** 2)) * ab)()
        p2 = ((bc @ bp / (abs(bc) ** 2)) * bc)()
        p3 = ((ca @ cp / (abs(ca) ** 2)) * ca)()
        return self.__class__(
            (p1[0] + self.__pa[0], p1[1] + self.__pa[1]),
            (p2[0] + self.__pb[0], p2[1] + self.__pb[1]),
            (p3[0] + self.__pc[0], p3[1] + self.__pc[1]),
        )

    def cevian_triangle(self, point: tuple[float, float], zord: int = 0) -> Self:
        """
        Constructs the cevian triangle associated with a given point.

        Parameters:
            point: Point of the cevian triangle.
            zord: Rendering priority of the new shape.

        Returns:
            Cevian triangle associated with `point`.
        """
        u, v, w = self.to_barycentric(point)
        return self.__class__(
            self.barycentric((0, v, w)),
            self.barycentric((u, 0, w)),
            self.barycentric((u, v, 0)),
            zord=zord,
        )

    def euler_line(self) -> Line:
        """
        Constructs the Euler line of the triangle (the line that joins the orthocenter,
        circumcenter, and centroid).
        """
        return Line.from_two_points(self.orthocenter, self.centroid)

    def __and__(self, other: Self | Line | Circle | Ellipse | Path | Parametric) -> Any:
        if isinstance(other, (self.__class__, Path, Parametric)):
            iss = []
            if isinstance(other, self.__class__):
                iss = [
                    intersect_segments(s1, s2, o1, o2)
                    for s1, s2 in combinations((self.__pa, self.__pb, self.__pc), 2)
                    for o1, o2 in combinations((other.A, other.B, other.C), 2)
                ]
            elif isinstance(other, Path):
                iss = [
                    intersect_segments(s1, s2, other.points[i], other.points[i + 1])
                    for s1, s2 in combinations((self.__pa, self.__pb, self.__pc), 2)
                    for i in range(len(other.points) - 1)
                ]
            elif isinstance(other, Parametric):
                ps = other.make_points()
                iss = [
                    intersect_segments(s1, s2, ps[i], ps[i + 1])
                    for s1, s2 in combinations((self.__pa, self.__pb, self.__pc), 2)
                    for i in range(len(ps) - 1)
                ]
            return (
                [
                    (
                        i
                        if isinstance(i[0], float)
                        else Path(
                            *cast(tuple[tuple[float, float], tuple[float, float]], i)
                        )
                    )
                    for i in iss
                    if i
                ]
                if len(iss)
                else None
            )
        if isinstance(other, Line):
            return _intersect_line_and_path(
                other, [self.__pa, self.__pb, self.__pc, self.__pa]
            )
        if isinstance(other, (Circle, Ellipse)):
            l1, l2, l3 = (
                Line.from_two_points(self.__pa, self.__pb),
                Line.from_two_points(self.__pb, self.__pc),
                Line.from_two_points(self.__pc, self.__pa),
            )
            ps = (
                _unpack_simple_intersection(l1 & other, self.__pa, self.__pb)
                + _unpack_simple_intersection(l2 & other, self.__pb, self.__pc)
                + _unpack_simple_intersection(l3 & other, self.__pc, self.__pa)
            )
            return ps if ps else None
        else:
            return NotImplemented

    def __rand__(
        self, other: Self | Line | Circle | Ellipse | Path | Parametric
    ) -> Any:
        return self & other


GenericBarycentric = Annotated[
    Callable[[Triangle], tuple[float, float, float]],
    "Barycentric coordinate parametrized on the triangle.",
]
GenericTrilinear = Annotated[
    Callable[[Triangle], tuple[float, float, float]],
    "Trilinear coordinate parametrized on the triangle.",
]
GenericCartesian = Annotated[
    Callable[[Triangle], tuple[float, float, float]],
    "Cartesian coordinate parametrized on the triangle.",
]
