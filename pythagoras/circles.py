from math import hypot, sqrt
from typing import Self

from .backend import (
    compile_options_svg,
    compile_options_tikz,
    svg_command,
    tikz_command,
)
from .pobject import PObject
from .utils import cartesian_to_canvas


class Circle(PObject):
    x: float
    y: float
    radius: float

    def __init__(self, x: float, y: float, radius: float, zord: int = 0) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self._zord = zord

    def tikz(self, *args: str, **kwargs: str | float) -> str:
        cmd = "filldraw" if "fill" in kwargs else "draw"
        compile_options_tikz(kwargs)
        return tikz_command(
            cmd, f"({self.x}, {self.y}) circle ({self.radius})", *args, **kwargs
        )

    def extrema(self) -> list[tuple[float, float]]:
        return [
            (self.x + self.radius, self.y + self.radius),
            (self.x + self.radius, self.y - self.radius),
            (self.x - self.radius, self.y + self.radius),
            (self.x - self.radius, self.y - self.radius),
        ]

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: str,
        **kwargs: str | float,
    ) -> str:
        cx, cy = cartesian_to_canvas(self.x, self.y, width, height, scale)
        cx -= origin[0]
        cy += origin[1]
        style: dict[str, str | float] = {
            "cx": cx,
            "cy": cy,
            "r": self.radius * scale,
            "fill": "none",
            "stroke": "black",
        }
        style.update(kwargs)
        compile_options_svg(style)
        return svg_command("circle", *args, **style)

    @classmethod
    def from_three_points(
        cls,
        p1: tuple[float, float],
        p2: tuple[float, float],
        p3: tuple[float, float],
        zord: int = 0,
    ) -> Self:
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
    def triangle_incenter(
        cls,
        p1: tuple[float, float],
        p2: tuple[float, float],
        p3: tuple[float, float],
        zord: int = 0,
    ) -> Self:
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

        return cls(ix, iy, area / s, zord)


class Point(Circle):
    def __init__(self, x: float, y: float, _radius: float = 1, zord: int = 0) -> None:
        super().__init__(x, y, _radius, zord)

    def tikz(self, *args: str, **kwargs: str | float) -> str:
        style: dict[str, str | float] = {"fill": "white", "color": "black"}
        style.update(kwargs)
        return super().tikz(*args, **style)

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: str,
        **kwargs: str | float,
    ) -> str:
        style: dict[str, str | float] = {"fill": "white", "color": "black"}
        style.update(kwargs)
        return super().svg(origin, width, height, scale, *args, **style)
