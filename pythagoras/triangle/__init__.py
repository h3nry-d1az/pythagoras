from math import acos, sqrt
from typing import Self

from ..backend import fill_default_args, svg_path, tikz_command
from ..circle import Circle
from ..pobject import PObject, POProperty, RenderingContext
from ..style.color import BLACK
from ..style.draw import Fill, Stroke
from ..utils import cartesian_to_canvas
from ..vector import Vector

__all__ = ["Triangle"]


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

    def circumcircle(self) -> Circle:
        """
        Produces the circumcircle of the triangle.
        Wrapper for :meth:`pythagoras.circle.Circle.triangle_circumcircle`.
        """
        return Circle.triangle_circumcircle(self.A, self.B, self.C, self._zord)

    @property
    def A(self) -> tuple[float, float]:
        """First of the points of the triangle; denoted by :math:`A`."""
        return self.__pa

    @property
    def B(self) -> tuple[float, float]:
        """Second of the points of the triangle; denoted by :math:`B`."""
        return self.__pb

    @property
    def C(self) -> tuple[float, float]:
        """Third of the points of the triangle; denoted by :math:`C`."""
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
        """Length of the side opposite to :math:`A`."""
        return self.__a

    @property
    def b(self) -> float:
        """Length of the side opposite to :math:`B`."""
        return self.__b

    @property
    def c(self) -> float:
        """Length of the side opposite to :math:`C`."""
        return self.__c

    @property
    def alpha(self) -> float:
        r"""
        Angle that corresponds to the vertex :math:`A`, i.e.,
        :math:`\alpha = \min\{\angle BAC, \angle CAB\}.`
        """
        return self.__alpha

    @property
    def beta(self) -> float:
        r"""
        Angle that corresponds to the vertex :math:`B`, i.e.,
        :math:`\beta = \min\{\angle ABC, \angle CBA\}.`
        """
        return self.__beta

    @property
    def gamma(self) -> float:
        r"""
        Angle that corresponds to the vertex :math:`C`, i.e.,
        :math:`\alpha = \min\{\angle ACB, \angle BCA\}.`
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
