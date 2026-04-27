from collections.abc import Callable
from math import inf

from .backend import compile_options_svg, compile_options_tikz, svg_path, tikz_command
from .pobject import PObject
from .utils import cartesian_to_canvas

__all__ = ["ParametricCurve"]


class ParametricCurve(PObject):
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
    ) -> None:
        self.f = f
        self.a = a
        self.b = b
        self.dt = dt if dt > 0 else (b - a) / 100

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
