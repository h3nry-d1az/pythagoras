from dataclasses import dataclass

from ..pobject import POProperty

__all__ = ["FillOpacity", "Opacity", "StrokeOpacity"]


@dataclass
class Opacity(POProperty):
    """
    Global opacity for an element.

    Attributes:
        opacity: Opacity value between 0 (transparent) and 1 (opaque).
    """

    opacity: float

    def svg(self) -> str:
        return f'opacity="{self.opacity:.4f}"'

    def tikz(self) -> str:
        return f"opacity={self.opacity:.4f}"


@dataclass
class FillOpacity(POProperty):
    """
    Opacity applied only to the fill of an element.

    Attributes:
        opacity: Fill opacity between 0 and 1.
    """

    opacity: float

    def svg(self) -> str:
        return f'fill-opacity="{self.opacity:.4f}"'

    def tikz(self) -> str:
        return f"fill opacity={self.opacity:.4f}"


@dataclass
class StrokeOpacity(POProperty):
    """
    Opacity applied only to the stroke (outline) of an element.

    Attributes:
        opacity: Stroke opacity between 0 and 1.
    """

    opacity: float

    def svg(self) -> str:
        return f'stroke-opacity="{self.opacity:.4f}"'

    def tikz(self) -> str:
        return f"draw opacity={self.opacity:.4f}"
