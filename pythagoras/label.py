from enum import Enum
from typing import Self

from latex2mathml.converter import convert

from .backend import tikz_command
from .pobject import PObject, POProperty, RenderingContext
from .style.draw import FontSize
from .utils import cartesian_to_canvas

__all__ = ["AnchoringDirection", "Label"]

_isqrt2 = 2**-0.5


class AnchoringDirection(Enum):
    """Anchoring directions. To be used when calling :meth:`Label.anchored`."""

    NORTH = (0, 1)
    SOUTH = (0, -1)
    EAST = (1, 0)
    WEST = (-1, 0)
    NORTH_EAST = (_isqrt2, _isqrt2)
    NORTH_WEST = (-_isqrt2, _isqrt2)
    SOUTH_EAST = (_isqrt2, -_isqrt2)
    SOUTH_WEST = (-_isqrt2, -_isqrt2)


class Label(PObject):
    r"""
    A text label rendered from :math:`{\rm \LaTeX}`.

    Attributes:
        x: :math:`x`-coordinate in Cartesian space.
        y: :math:`y`-coordinate in Cartesian space.
        tag: :math:`{\rm \LaTeX}` string to render inside the label.
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

    @classmethod
    def anchored(
        cls,
        point: tuple[float, float],
        direction: AnchoringDirection,
        tag: str,
        offset: float = 0.25,
        padding: float = 0.05,
        zord: int = 0,
    ) -> Self:
        r"""
        Creates a label anchored to a given point in :math:`\mathbf R^2`.

        Parameters:
            point: Point to which the label is anchored.
            direction: Anchoring direction (north, west...). See :class:`AnchoringDirection` for further information.
            tag: :math:`{\rm \LaTeX}` string to render inside the label.
            offset: Distance between the point to which the label is anchored and the label itself (default 0.25).
            padding: Spacing around the label (default 0.05).
            zord: Rendering priority.
        """
        return cls(
            point[0] + direction.value[0] * offset,
            point[1] + direction.value[1] * offset,
            tag,
            padding,
            zord,
        )

    def extrema(self) -> list[tuple[float, float]]:
        return [
            (self.x - self.padding, self.y + self.padding),
            (self.x + self.padding * len(self.tag), self.y + self.padding),
            (self.x - self.padding, self.y - self.padding),
            (self.x + self.padding * len(self.tag), self.y - self.padding),
        ]

    def tikz(self, ctx: RenderingContext, *args: POProperty) -> str:
        return tikz_command(
            "node", f"at ({self.x}, {self.y}) {{{f'${self.tag}$'}}}", *args
        )

    def svg(self, ctx: RenderingContext, *args: POProperty) -> str:
        x, y = cartesian_to_canvas((self.x, self.y), ctx)
        w, h = min(ctx.width - x, x), min(ctx.height - y, y)
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
