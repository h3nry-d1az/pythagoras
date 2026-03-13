from typing import Self

from .backend import (
    compile_options_svg,
    compile_options_tikz,
    svg_command,
    tikz_command,
)
from .pobject import PObject


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

    def svg(self, *args: str, **kwargs: str | float) -> str:
        style: dict[str, str | float] = {"cx": self.x, "cy": self.y, "r": self.radius}
        style.update(kwargs)
        compile_options_svg(style)
        return svg_command("circle", *args, **style)

    @classmethod
    def from_three_points(
        cls, p1: tuple[int, int], p2: tuple[int, int], p3: tuple[int, int]
    ) -> Self:
        return cls(0, 0, 0)


class Point(Circle):
    def __init__(self, x: float, y: float, _radius: float = 1, zord: int = 0) -> None:
        super().__init__(x, y, _radius, zord)

    def tikz(self, *args: str, **kwargs: str | float) -> str:
        return super().tikz(*args, fill="white", color="black", **kwargs)

    def svg(self, *args: str, **kwargs: str | float) -> str:
        return super().svg(*args, fill="white", color="black", **kwargs)
