from latex2mathml.converter import convert

from .backend import tikz_command
from .pobject import PObject, POProperty
from .style.draw import FontSize
from .utils import cartesian_to_canvas

__all__ = ["Label"]


class Label(PObject):
    r"""
    A text label rendered from $\LaTeX$.

    Attributes:
        x: $x$-coordinate in Cartesian space.
        y: $y$-coordinate in Cartesian space.
        tag: $\LaTeX$ string to render inside the label.
        padding: Spacing around the label (default 0.05).
        zord: Drawing order; higher values are drawn later.
    """

    x: float
    y: float
    tag: str
    padding: float

    def __init__(
        self, x: float, y: float, tag: str, padding: float = 0.05, zord: int = 0
    ) -> None:
        self.x = x
        self.y = y
        self.tag = tag
        self.padding = padding
        self._zord = zord

    def extrema(self) -> list[tuple[float, float]]:
        return [
            (self.x - self.padding, self.y + self.padding),
            (self.x + self.padding * len(self.tag), self.y + self.padding),
            (self.x - self.padding, self.y - self.padding),
            (self.x + self.padding * len(self.tag), self.y - self.padding),
        ]

    def tikz(self, *args: POProperty) -> str:
        return tikz_command(
            "node", f"at ({self.x}, {self.y}) {{{f'${self.tag}$'}}}", *args
        )

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: POProperty,
    ) -> str:
        x, y = cartesian_to_canvas(self.x, self.y, width, height, scale)
        x -= origin[0]
        y += origin[1]
        w, h = min(width - x, x), min(height - y, y)
        px, py = x - w, y - h
        fs = None
        for p in args:
            if isinstance(p, FontSize):
                fs = p
                break
        return (
            f'<foreignObject x="{px:.4f}" y="{py:.4f}" width="{2 * w:.4f}" height="{2 * h:.4f}">\n'
            f'<div xmlns="http://www.w3.org/1999/xhtml" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;{f" font-size: {fs.size}{fs.unit};" if fs else ""}">\n'
            f"{convert(self.tag)}"
            "</div>"
            "</foreignObject>"
        )
