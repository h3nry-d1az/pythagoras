from dataclasses import dataclass

from ..pobject import POProperty
from .color import Color

__all__ = ["Fill", "LineWidth", "Stroke"]


@dataclass
class Fill(POProperty):
    """
    Fill style for shapes.

    Attributes:
        color: Fill color. If `None`, the shape is not filled.
    """

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
    """
    Stroke (outline) style for shapes.

    Attributes:
        color: Stroke color. If `None`, no stroke is drawn.
    """

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
    """
    Line width specification for strokes.

    Attributes:
        width: Line width magnitude.
        unit: Unit for the width (default: 'pt').
    """

    width: int
    unit: str = "pt"

    def svg(self) -> str:
        return f'stroke-width="{self.width}{self.unit}"'

    def tikz(self) -> str:
        return f"line width={self.width}{self.unit}"


@dataclass
class FontSize(POProperty):
    """
    Font size specifier.

    Attributes:
        size: Font size value.
        unit: Unit for the font size (default: 'pt').
    """

    size: float
    unit: str = "pt"

    def svg(self) -> str:
        return f'font-size="{self.size}"'

    def tikz(self) -> str:
        return rf"font=\fontsize{{{self.size}{self.unit}}}{{{self.size * 1.2:.4f}{self.unit}}}\selectfont"
