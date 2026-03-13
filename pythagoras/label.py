from latex2mathml.converter import convert

from .backend import compile_options_svg, compile_options_tikz, tikz_command
from .pobject import PObject
from .utils import cartesian_to_canvas


class Label(PObject):
    x: float
    y: float
    tag: str

    def __init__(self, x: float, y: float, tag: str, zord: int = 0) -> None:
        self.x = x
        self.y = y
        self.tag = tag
        self._zord = zord

    def tikz(self, *args: str, **kwargs: str | float) -> str:
        compile_options_tikz(kwargs)
        return tikz_command("node", f"at ({self.x}, {self.y}) {{{f'${self.tag}$'}}}")

    def svg(
        self,
        width: float,
        height: float,
        scale: float,
        *args: str,
        **kwargs: str | float,
    ) -> str:
        x, y = cartesian_to_canvas(self.x, self.y, width, height, scale)
        w, h = min(width - x, x), min(height - y, y)
        px, py = x - w, y - h
        compile_options_svg(kwargs)
        fs = kwargs.get("font_scale", scale)
        return (
            f'<foreignObject x="{px}" y="{py}" width="{2 * w}" height="{2 * h}">\n'
            f'<div xmlns="http://www.w3.org/1999/xhtml" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: {12 * fs}px;">\n'
            f"{convert(self.tag)}"
            "</div>"
            "</foreignObject>"
        )
