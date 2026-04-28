from collections.abc import Callable
from math import atan2, cos, degrees, hypot, inf, pi, sin, tau
from typing import Self

from .backend import (
    compile_options_svg,
    compile_options_tikz,
    svg_command,
    svg_path,
    tikz_command,
)
from .pobject import PObject
from .utils import cartesian_to_canvas

__all__ = ["Arc", "Parametric"]


class Arc(PObject):
    o: tuple[float, float]
    p: tuple[float, float]
    theta: float

    def __init__(
        self,
        o: tuple[float, float],
        p: tuple[float, float],
        theta: float,
        zord: int = 0,
    ) -> None:
        self.o = o
        self.p = p
        self.theta = theta
        self._zord = zord

    @classmethod
    def from_three_points(
        cls,
        p1: tuple[float, float],
        p2: tuple[float, float],
        p3: tuple[float, float],
        zord: int = 0,
    ) -> Self:
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        x3, y3 = p3[0], p3[1]
        D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

        if abs(D) < 1e-10:
            raise ValueError("The three points are collinear. No arc can be formed.")

        sq1 = x1**2 + y1**2
        sq2 = x2**2 + y2**2
        sq3 = x3**2 + y3**2
        cx = (sq1 * (y2 - y3) + sq2 * (y3 - y1) + sq3 * (y1 - y2)) / D
        cy = (sq1 * (x3 - x2) + sq2 * (x1 - x3) + sq3 * (x2 - x1)) / D
        ang1 = atan2(y1 - cy, x1 - cx)
        ang2 = atan2(y2 - cy, x2 - cx)
        ang3 = atan2(y3 - cy, x3 - cx)
        sweep_ccw = (ang3 - ang1) % tau
        dist_to_mid = (ang2 - ang1) % tau
        theta = sweep_ccw if dist_to_mid < sweep_ccw else sweep_ccw - tau
        return cls((cx, cy), p1, theta, zord)

    @classmethod
    def from_two_points_and_angle(
        cls, p1: tuple[float, float], p2: tuple[float, float], theta: float
    ) -> Self:
        return cls(((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2), p1, theta)

    @property
    def radius(self) -> float:
        x, y = self.p[0] - self.o[0], self.p[1] - self.o[1]
        return hypot(x, y)

    @property
    def end_point(self) -> tuple[float, float]:
        x, y = self.p[0] - self.o[0], self.p[1] - self.o[1]
        return (
            x * cos(self.theta) - y * sin(self.theta) + self.o[0],
            x * sin(self.theta) + y * cos(self.theta) + self.o[1],
        )

    def extrema(self) -> list[tuple[float, float]]:
        r = self.radius
        x, y = self.p[0] - self.o[0], self.p[1] - self.o[1]
        theta1 = atan2(y, x)
        theta2 = theta1 + self.theta

        ex = self.o[0] + r * cos(theta2)
        ey = self.o[1] + r * sin(theta2)
        x_min = min(self.p[0], ex)
        x_max = max(self.p[0], ex)
        y_min = min(self.p[1], ey)
        y_max = max(self.p[1], ey)

        def crosses_angle(target_angle: float) -> bool:
            if abs(self.theta) >= tau:
                return True
            start_angle = theta1 if self.theta > 0 else theta2
            sweep = abs(self.theta)
            angular_distance = (target_angle - start_angle) % tau
            return angular_distance <= sweep

        if crosses_angle(0.0):
            x_max = self.o[0] + r
        if crosses_angle(pi / 2):
            y_max = self.o[1] + r
        if crosses_angle(pi):
            x_min = self.o[0] - r
        if crosses_angle(3 * pi / 2):
            y_min = self.o[1] - r
        return [(x_min, y_min), (x_max, y_max)]

    def tikz(self, *args: str, **kwargs: str | float) -> str:
        compile_options_tikz(kwargs)
        x, y = self.p[0] - self.o[0], self.p[1] - self.o[1]
        alpha = atan2(y, x)
        beta = alpha + self.theta
        return tikz_command(
            "draw",
            *args,
            *kwargs,
            f"({self.p[0]}, {self.p[1]}) arc ({degrees(alpha)}:{degrees(beta)}:{self.radius})",
        )

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: str,
        **kwargs: str | float,
    ) -> str:
        compile_options_svg(kwargs)
        style: dict[str, str | float] = {"fill": "none", "stroke": "black"}
        style.update(kwargs)
        r = self.radius * scale
        px, py = cartesian_to_canvas(*self.p, width, height, scale)
        ex, ey = cartesian_to_canvas(*self.end_point, width, height, scale)
        px -= origin[0]
        py += origin[1]
        ex -= origin[0]
        ey += origin[1]
        return svg_command(
            "path",
            *args,
            d=f"M {px:.8f} {py:.8f} A {r:.8f} {r:.8f} 0 {1 if abs(self.theta) >= pi else 0} 0 {ex:.4f} {ey:.4f}",
            **style,
        )


class Parametric(PObject):
    f: Callable[[float], tuple[float, float]]
    a: float
    b: float
    dt: float

    def __init__(
        self,
        f: Callable[[float], tuple[float, float]],
        a: float,
        b: float,
        dt: float = 0,
        zord: int = 0,
    ) -> None:
        self.f = f
        self.a = a
        self.b = b
        self.dt = dt if dt > 0 else (b - a) / 100
        self._zord = zord

    def make_points(self) -> list[tuple[float, float]]:
        ps: list[tuple[float, float]] = []
        t = self.a
        while t <= self.b:
            t += self.dt
            ps.append(self.f(t))
        return ps

    def extrema(self) -> list[tuple[float, float]]:
        mxx, mxy, mnx, mny = -inf, -inf, inf, inf
        for p in self.make_points():
            if p[0] < mnx:
                mnx = p[0]
            if p[0] > mxx:
                mxx = p[0]
            if p[1] < mny:
                mny = p[1]
            if p[1] > mxy:
                mxy = p[1]
        return [(mnx, mny), (mxx, mxy)]

    def tikz(self, *args: str, **kwargs: str | float) -> str:
        compile_options_tikz(kwargs)
        return tikz_command(
            "draw",
            " -- ".join(f"({p[0]}, {p[1]})" for p in self.make_points()),
            *args,
            **kwargs,
        )

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: str,
        **kwargs: str | float,
    ) -> str:
        compile_options_svg(kwargs)
        style: dict[str, str | float] = {"fill": "none", "stroke": "black"}
        style.update(kwargs)
        return svg_path(
            (cartesian_to_canvas(*p, width, height, scale) for p in self.make_points()),
            origin,
            width,
            height,
            scale,
            *args,
            **style,
        )
