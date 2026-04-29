from dataclasses import dataclass

from ..pobject import POProperty
from .color import Color


@dataclass
class Fill(POProperty):
    color: Color | None

    def svg(self) -> str:
        return f'fill="{self.color.svg()}"' if isinstance(self.color, Color) else ""

    def tikz(self) -> str:
        return f"fill={self.color.tikz()}" if isinstance(self.color, Color) else ""


@dataclass
class Stroke(POProperty):
    color: Color | None

    def svg(self) -> str:
        return f'stroke="{self.color.svg()}"' if isinstance(self.color, Color) else ""

    def tikz(self) -> str:
        return f"draw={self.color.tikz()}" if isinstance(self.color, Color) else ""


@dataclass
class LineWidth(POProperty):
    width: int
    unit: str = "mm"

    def svg(self) -> str:
        return f'stroke-width="{self.width}{self.unit}"'

    def tikz(self) -> str:
        return f"line width={self.width}{self.unit}"
