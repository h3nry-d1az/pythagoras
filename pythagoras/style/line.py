from dataclasses import dataclass
from typing import Self

from ..pobject import POProperty

__all__ = ["Dashed"]


@dataclass
class Dashed(POProperty):
    """
    Dash pattern for stroked lines.

    Attributes:
        dash: Dash length.
        gap: Gap length between dashes.
        unit: Unit for dash/gap (default: 'pt').
        round: Use rounded line caps when `True`.
    """

    dash: float = 2
    gap: float = 2
    unit: str = "pt"
    round: bool = False

    @classmethod
    def dotted(cls, width: float = 1, round: bool = True) -> Self:
        return cls(width, 2 * width, "pt", round)

    def svg(self) -> str:
        return f'stroke-dasharray="{self.dash}{self.unit} {self.gap}{self.unit}"' + (
            ' stroke-linecap="round"' if self.round else ""
        )

    def tikz(self) -> str:
        return f"dash pattern=on {self.dash}{self.unit} off {self.gap}{self.unit}" + (
            ", line cap=round" if self.round else ""
        )
