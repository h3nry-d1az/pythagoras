from dataclasses import dataclass

from ..pobject import POProperty

__all__ = ["FillOpacity", "Opacity", "StrokeOpacity"]


@dataclass
class Opacity(POProperty):
    opacity: float

    def svg(self) -> str:
        return f'opacity="{self.opacity:.4f}"'

    def tikz(self) -> str:
        return f"opacity={self.opacity:.4f}"


@dataclass
class FillOpacity(POProperty):
    opacity: float

    def svg(self) -> str:
        return f'fill-opacity="{self.opacity:.4f}"'

    def tikz(self) -> str:
        return f"fill opacity={self.opacity:.4f}"


@dataclass
class StrokeOpacity(POProperty):
    opacity: float

    def svg(self) -> str:
        return f'stroke-opacity="{self.opacity:.4f}"'

    def tikz(self) -> str:
        return f"draw opacity={self.opacity:.4f}"
