from dataclasses import dataclass

from ..pobject import POProperty
from .color import Color

__all__ = ["Fill", "LineWidth", "Stroke"]


@dataclass
class Fill(POProperty):
    color: Color | None

    def svg(self) -> str:
        return (
            f'fill="{self.color.svg()}"'
            if isinstance(self.color, Color)
            else 'fill="none"'
        )

    def tikz(self) -> str:
        return f"fill={self.color.tikz()}" if isinstance(self.color, Color) else ""


@dataclass
class Stroke(POProperty):
    color: Color | None

    def svg(self) -> str:
        return (
            f'stroke="{self.color.svg()}"'
            if isinstance(self.color, Color)
            else 'stroke="none"'
        )

    def tikz(self) -> str:
        return f"draw={self.color.tikz()}" if isinstance(self.color, Color) else ""


@dataclass
class LineWidth(POProperty):
    width: int
    unit: str = "pt"

    def svg(self) -> str:
        return f'stroke-width="{self.width}{self.unit}"'

    def tikz(self) -> str:
        return f"line width={self.width}{self.unit}"


@dataclass
class FontSize(POProperty):
    size: float
    unit: str = "pt"

    def svg(self) -> str:
        return f'font-size="{self.size}"'

    def tikz(self) -> str:
        return rf"font=\fontsize{{{self.size}{self.unit}}}{{{self.size * 1.2:.4f}{self.unit}}}\selectfont"
