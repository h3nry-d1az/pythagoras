from latex2mathml.converter import convert

from .backend import compile_options_svg, compile_options_tikz, tikz_command
from .pobject import PObject
from .utils import cartesian_to_canvas

__all__ = ["Label"]


class Label(PObject):
    x: float
    y: float
    tag: str

    def __init__(self, x: float, y: float, tag: str, zord: int = 0) -> None:
        self.x = x
        self.y = y
        self.tag = tag
        self._zord = zord

    def extrema(self) -> list[tuple[float, float]]:
        return [(self.x, self.y)]

    def tikz(self, *args: str, **kwargs: str | float) -> str:
        compile_options_tikz(kwargs)
        return tikz_command("node", f"at ({self.x}, {self.y}) {{{f'${self.tag}$'}}}")

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: str,
        **kwargs: str | float,
    ) -> str:
        x, y = cartesian_to_canvas(self.x, self.y, width, height, scale)
        x -= origin[0]
        y += origin[1]
        w, h = min(width - x, x), min(height - y, y)
        px, py = x - w, y - h
        compile_options_svg(kwargs)
        fs = kwargs.get("font_scale", scale)
        return (
            f'<foreignObject x="{px:.4f}" y="{py:.4f}" width="{2 * w:.4f}" height="{2 * h:.4f}">\n'
            f'<div xmlns="http://www.w3.org/1999/xhtml" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: {12 * fs:.4f}px;">\n'
            f"{convert(self.tag)}"
            "</div>"
            "</foreignObject>"
        )
