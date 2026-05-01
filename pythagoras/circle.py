from math import atan2, cos, degrees, hypot, radians, sin, sqrt
from typing import Self

from .backend import fill_default_args, svg_command, tikz_command
from .pobject import PObject, POProperty
from .style import CustomStyle, color
from .style.draw import Fill, Stroke
from .utils import cartesian_to_canvas

__all__ = ["Circle", "Ellipse", "Point"]


class Circle(PObject):
    """
    Circle `PObject`. As its name suggests, renders into a cirlce when drawn.

    Attributes:
        x: :math:`x`-coordinate of the center.
        y: :math:`y`-coordinate of the center.
        radius: Radius.
    """

    x: float
    y: float
    radius: float

    def __init__(self, x: float, y: float, radius: float, zord: int = 0) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self._zord = zord

    def extrema(self) -> list[tuple[float, float]]:
        return [
            (self.x + self.radius, self.y + self.radius),
            (self.x + self.radius, self.y - self.radius),
            (self.x - self.radius, self.y + self.radius),
            (self.x - self.radius, self.y - self.radius),
        ]

    def tikz(self, *args: POProperty) -> str:
        cmd = "filldraw" if any(isinstance(x, Fill) for x in args) else "draw"
        return tikz_command(cmd, f"({self.x}, {self.y}) circle ({self.radius})", *args)

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: POProperty,
    ) -> str:
        cx, cy = cartesian_to_canvas(self.x, self.y, width, height, scale)
        cx -= origin[0]
        cy += origin[1]
        args = (
            CustomStyle("cx", cx),
            CustomStyle("cy", cy),
            CustomStyle("r", self.radius * scale),
            *args,
        )
        return svg_command(
            "circle",
            *fill_default_args(args, (Fill, Fill(None)), (Stroke, Stroke(color.BLACK))),
        )

    @classmethod
    def triangle_circumcircle(
        cls,
        p1: tuple[float, float],
        p2: tuple[float, float],
        p3: tuple[float, float],
        zord: int = 0,
    ) -> Self:
        """
        Generate the circle that passes through three given points. Recall that the
        circumcircle of a triangle is the intersection of the side bisectors; this is
        the way it is found.

        Parameters:
            p1: First point of the triangle.
            p2: Second point of the triangle.
            p3: Third point of the triangle.
            zord: Rendering priority of the circle.

        Returns:
            A circle that passes through `p1`, `p2` and `p3`.
        """
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        m1 = x1**2 + y1**2
        m2 = x2**2 + y2**2
        m3 = x3**2 + y3**2

        a = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2

        if abs(a) < 1e-10:
            raise ValueError("Points are collinear; a circle cannot be formed.")

        b = m1 * (y3 - y2) + m2 * (y1 - y3) + m3 * (y2 - y1)
        c = m1 * (x2 - x3) + m2 * (x3 - x1) + m3 * (x1 - x2)

        xc = -b / (2 * a)
        yc = -c / (2 * a)
        r = hypot(xc - x1, yc - y1)

        return cls(xc, yc, r, zord)

    @classmethod
    def triangle_incircle(
        cls,
        p1: tuple[float, float],
        p2: tuple[float, float],
        p3: tuple[float, float],
        zord: int = 0,
    ) -> tuple[Self, tuple[float, float], tuple[float, float], tuple[float, float]]:
        """
        Computes the points of tangency and the center of the incircle of the triangle
        delimited by three points. The incircle of a triangle is computed as the intersection
        of its angle bisectors.

        Parameters:
            p1: First point of the triangle.
            p2: Second point of the triangle.
            p3: Third point of the triangle.
            zord: Rendering priority of the circle.

        Returns:
            The incircle together with the three points of tangency.
        """
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        d1 = hypot(x2 - x3, y2 - y3)
        d2 = hypot(x1 - x3, y1 - y3)
        d3 = hypot(x1 - x2, y1 - y2)
        s = (d1 + d2 + d3) / 2
        area = sqrt(abs(s * (s - d1) * (s - d2) * (s - d3)))

        ix = (d1 * x1 + d2 * x2 + d3 * x3) / (2 * s)
        iy = (d1 * y1 + d2 * y2 + d3 * y3) / (2 * s)

        q1 = (s - d1) / d3
        q2 = (s - d2) / d1
        q3 = (s - d3) / d2

        return (
            cls(ix, iy, area / s, zord),
            (p1[0] + (p2[0] - p1[0]) * q1, p1[1] + (p2[1] - p1[1]) * q1),
            (p2[0] + (p3[0] - p2[0]) * q2, p2[1] + (p3[1] - p2[1]) * q2),
            (p3[0] + (p1[0] - p3[0]) * q3, p3[1] + (p1[1] - p3[1]) * q3),
        )


class Ellipse(PObject):
    """
    An ellipse.

    Attributes:
        x: :math:`x`-coordinate of its center.
        y: :math:`y`-coordinate of its center.
        rx: Length of the semi axis corresponding to the :math:`x` axis.
        ry: Length of the semi axis corresponding to the :math:`y` axis.
        theta: Angle of rotation with respect to the positive :math:`x` axis.
    """

    x: float
    y: float
    rx: float
    ry: float
    theta: float

    def __init__(self, x: float, y: float, rx: float, ry: float, zord: int = 0) -> None:
        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry
        self.theta = 0
        self._zord = zord

    def extrema(self) -> list[tuple[float, float]]:
        dx = hypot(
            self.rx * cos(radians(self.theta)), self.ry * sin(radians(self.theta))
        )
        dy = hypot(
            self.rx * sin(radians(self.theta)), self.ry * cos(radians(self.theta))
        )
        return [
            (self.x + dx, self.y + dy),
            (self.x + dx, self.y - dy),
            (self.x - dx, self.y + dy),
            (self.x - dx, self.y - dy),
        ]

    def tikz(self, *args: POProperty) -> str:
        cmd = "filldraw" if any(isinstance(x, Fill) for x in args) else "draw"
        return tikz_command(
            cmd,
            f"({self.x}, {self.y}) ellipse [x radius={self.rx}, y radius={self.ry}, rotate={self.theta}]",
            *args,
        )

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: POProperty,
    ) -> str:
        cx, cy = cartesian_to_canvas(self.x, self.y, width, height, scale)
        cx -= origin[0]
        cy += origin[1]
        args = (
            CustomStyle("cx", cx),
            CustomStyle("cy", cy),
            CustomStyle("rx", self.rx * scale),
            CustomStyle("ry", self.ry * scale),
            CustomStyle("transform", f"rotate({-self.theta:.4f}, {cx:.4f}, {cy:.4f})"),
            *args,
        )
        return svg_command(
            "ellipse",
            *fill_default_args(args, (Fill, Fill(None)), (Stroke, Stroke(color.BLACK))),
        )

    @classmethod
    def from_foci(
        cls,
        f1: tuple[float, float],
        f2: tuple[float, float],
        p: tuple[float, float],
        zord: int = 0,
    ) -> Self:
        """
        Creates an ellipse from its center and foci.

        Parameters:
            f1: First focus point.
            f2: Second focus point.
            p: Center of the ellipse.

        Returns:
            Ellipse with the given foci and center.
        """
        x = (f1[0] + f2[0]) / 2
        y = (f1[1] + f2[1]) / 2
        c = hypot(f1[0] - f2[0], f1[1] - f2[1]) / 2
        rx = (hypot(f1[0] - p[0], f1[1] - p[1]) + hypot(f2[0] - p[0], f2[1] - p[1])) / 2
        ry = sqrt(rx**2 - c**2) if rx > c else 0
        ell = cls(x, y, rx, ry, zord)
        ell.theta = degrees(atan2(f2[1] - f1[1], f2[0] - f1[0]))
        return ell


class Point(Circle):
    """
    A circle small enough to represent a point.
    """

    def __init__(self, x: float, y: float, radius: float = 1, zord: int = 0) -> None:
        super().__init__(x, y, radius, zord)

    def tikz(self, *args: POProperty) -> str:
        return super().tikz(
            *fill_default_args(
                args, (Fill, Fill(color.WHITE)), (Stroke, Stroke(color.BLACK))
            )
        )

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: POProperty,
    ) -> str:
        return super().svg(
            origin,
            width,
            height,
            scale,
            *fill_default_args(
                args, (Fill, Fill(color.WHITE)), (Stroke, Stroke(color.BLACK))
            ),
        )
