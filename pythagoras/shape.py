from math import cos, radians, sin, sqrt, tau
from typing import Self

from .backend import compile_options_svg, compile_options_tikz, svg_path, tikz_command
from .pobject import PObject
from .utils import cartesian_to_canvas

__all__ = ["Path", "Polygon"]


class Path(PObject):
    points: list[tuple[float, float]]

    def __init__(self, *args: tuple[float, float], zord: int = 0) -> None:
        self.points = list(args)
        self._zord = zord
        if len(self.points) < 2:
            raise RuntimeError("A path must have at least two points.")

    def extrema(self) -> list[tuple[float, float]]:
        return self.points

    def tikz(self, *args: str, **kwargs: str | float) -> str:
        compile_options_tikz(kwargs)
        return tikz_command(
            "draw",
            " -- ".join(f"({p[0]}, {p[1]})" for p in self.points),
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
            (cartesian_to_canvas(*p, width, height, scale) for p in self.points),
            origin,
            width,
            height,
            scale,
            *args,
            **style,
        )

    def rotate(self, point: tuple[float, float], theta: float) -> None:
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
    def tikz(self, *args: str, **kwargs: str | float) -> str:
        compile_options_tikz(kwargs)
        return tikz_command(
            "draw",
            " -- ".join(f"({p[0]}, {p[1]})" for p in self.points) + " -- cycle",
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
        self.points.append(self.points[0])
        code = super().svg(origin, width, height, scale, *args, **kwargs)
        self.points.pop()
        return code

    @classmethod
    def regular(cls, x: float, y: float, r: float, n: int, zord: int = 0) -> Self:
        ps = ((x + r * cos(i * tau / n), y + r * sin(i * tau / n)) for i in range(n))
        return cls(*ps, zord=zord)

    @classmethod
    def triangle_from_lengths(cls, a: float, b: float, c: float, zord: int = 0) -> Self:
        a, b, c = sorted([a, b, c])
        if a + b <= c:
            raise ValueError("The given lengths cannot form a valid triangle.")
        x = (c**2 + b**2 - a**2) / (2 * c)
        y = sqrt(abs(b**2 - x**2))
        cx = (0 + c + x) / 3
        cy = y / 3
        return cls((-cx, -cy), (c - cx, -cy), (x - cx, y - cy), zord=zord)
