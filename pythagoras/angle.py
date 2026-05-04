from math import atan2, ceil, cos, degrees, floor, hypot, pi, radians, sin

from .backend import fill_default_args, svg_command, svg_path, tikz_command
from .pobject import PObject, POProperty, RenderingContext
from .style import CustomStyle, color
from .style.draw import Fill, Stroke
from .utils import cartesian_to_canvas

__all__ = ["Angle", "RAngle"]


class Angle(PObject):
    """
    An angle described by three points and its radius, following the right-hand rule.

    Attributes:
        p1: Starting point.
        p2: Corner of the angle.
        p3: End point.
        radius: Radius of the arc.
    """

    p1: tuple[float, float]
    p2: tuple[float, float]
    p3: tuple[float, float]
    radius: float

    def __init__(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        p3: tuple[float, float],
        radius: float = 1,
        zord: int = 0,
    ) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.radius = radius
        self._zord = zord

    def extrema(self) -> list[tuple[float, float]]:
        v1x, v1y = self.p1[0] - self.p2[0], self.p1[1] - self.p2[1]
        v2x, v2y = self.p3[0] - self.p2[0], self.p3[1] - self.p2[1]

        mag1 = hypot(v1x, v1y)
        mag2 = hypot(v2x, v2y)

        if mag1 == 0 or mag2 == 0:
            return [self.p2]

        extrema = [
            self.p2,
            (
                self.p2[0] + self.radius * (v1x / mag1),
                self.p2[1] + self.radius * (v1y / mag1),
            ),
            (
                self.p2[0] + self.radius * (v2x / mag2),
                self.p2[1] + self.radius * (v2y / mag2),
            ),
        ]

        theta1 = atan2(v1y, v1x)
        theta2 = atan2(v2y, v2x)

        if theta2 < theta1:
            theta2 += 2 * pi

        for k in range(ceil(theta1 / (pi / 2)), floor(theta2 / (pi / 2)) + 1):
            angle = k * (pi / 2)
            cx = self.p2[0] + self.radius * cos(angle)
            cy = self.p2[1] + self.radius * sin(angle)
            extrema.append((cx, cy))

        return extrema

    def tikz(self, ctx: RenderingContext, *args: POProperty) -> str:
        v1x, v1y = self.p1[0] - self.p2[0], self.p1[1] - self.p2[1]
        v2x, v2y = self.p3[0] - self.p2[0], self.p3[1] - self.p2[1]

        deg1 = degrees(atan2(v1y, v1x))
        deg2 = degrees(atan2(v2y, v2x))
        deg1 += 360 if deg1 < 0 else 0
        deg2 += 360 if deg2 < 0 else 0
        if deg2 < deg1:
            deg2 += 360

        start_x = self.p2[0] + self.radius * cos(radians(deg1))
        start_y = self.p2[1] + self.radius * sin(radians(deg1))

        return tikz_command(
            "draw", f"({start_x}, {start_y}) arc ({deg1}:{deg2}:{self.radius})", *args
        )

    def svg(self, ctx: RenderingContext, *args: POProperty) -> str:
        ax_c, ay_c = cartesian_to_canvas(self.p1, ctx)
        bx_c, by_c = cartesian_to_canvas(self.p2, ctx)
        cx_c, cy_c = cartesian_to_canvas(self.p3, ctx)

        v1 = (ax_c - bx_c, ay_c - by_c)
        v2 = (cx_c - bx_c, cy_c - by_c)

        mag1 = hypot(v1[0], v1[1])
        mag2 = hypot(v2[0], v2[1])

        if mag1 == 0 or mag2 == 0:
            raise ValueError("Invalid angle.")

        start_x = bx_c + self.radius * ctx.scale * (v1[0] / mag1)
        start_y = by_c + self.radius * ctx.scale * (v1[1] / mag1)

        end_x = bx_c + self.radius * ctx.scale * (v2[0] / mag2)
        end_y = by_c + self.radius * ctx.scale * (v2[1] / mag2)

        sweep_angle = (
            atan2(self.p3[1] - self.p2[1], self.p3[0] - self.p2[0])
            - atan2(self.p1[1] - self.p2[1], self.p1[0] - self.p2[0])
        ) % (2 * pi)
        large_arc_flag = 1 if sweep_angle > pi else 0
        sweep_flag = 0

        d = f"M {start_x:.4f} {start_y:.4f} A {self.radius * ctx.scale:.4f} {self.radius * ctx.scale:.4f} 0 {large_arc_flag} {sweep_flag} {end_x:.4f} {end_y:.4f}"
        return svg_command(
            "path",
            CustomStyle("d", d),
            *fill_default_args(args, (Fill, Fill(None)), (Stroke, Stroke(color.BLACK))),
        )


class RAngle(Angle):
    """
    A special type of :class:`Angle` instance, where the shape is drawn with straight lines instead of an arc.
    This results in a square whenever the angle measures 90 degrees, and a rhombus otherwise.
    """

    def extrema(self) -> list[tuple[float, float]]:
        rn = self.radius / (2 ** (1 / 2))

        v1 = (self.p1[0] - self.p2[0], self.p1[1] - self.p2[1])
        n1 = hypot(*v1)
        u1 = (v1[0] / n1, v1[1] / n1)

        v2 = (self.p3[0] - self.p2[0], self.p3[1] - self.p2[1])
        n2 = hypot(*v2)
        u2 = (v2[0] / n2, v2[1] / n2)

        return [
            self.p2,
            (self.p2[0] + u1[0] * rn, self.p2[1] + u1[1] * rn),
            (self.p2[0] + (u1[0] + u2[0]) * rn, self.p2[1] + (u1[1] + u2[1]) * rn),
            (self.p2[0] + u2[0] * rn, self.p2[1] + u2[1] * rn),
        ]

    def tikz(self, ctx: RenderingContext, *args: POProperty) -> str:
        points = self.extrema()
        points.append(points[0])
        return tikz_command(
            "draw", " -- ".join(f"({p[0]}, {p[1]})" for p in points), *args
        )

    def svg(self, ctx: RenderingContext, *args: POProperty) -> str:
        points = self.extrema()
        points.append(points[0])
        return svg_path(
            (cartesian_to_canvas(p, ctx) for p in points),
            *fill_default_args(args, (Fill, Fill(None)), (Stroke, Stroke(color.BLACK))),
        )
