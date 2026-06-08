from collections.abc import Iterable
from math import ceil

from .pobject import POProperty, RenderingContext
from .style import CustomStyle
from .style.color import Color
from .style.draw import Fill, FontSize, LineWidth, Stroke
from .style.line import Dashed
from .style.opacity import FillOpacity, Opacity, StrokeOpacity

__all__ = [
    "RasterPicture",
    "fill_default_args",
    "svg_command",
    "svg_path",
    "tikz_command",
]


def tikz_command(name: str, body: str, *args: POProperty) -> str:
    r"""
    Put together a TikZ command from its components.

    Parameters:
        name: Name of the command, that is, `\\{name}`.
        body: What goes between the command arguments and the final semicolon.
        *args: Arguments of the command -- i.e., `\\{name}[args]` -- as :class:`POProperty<pythagoras.pobject.POProperty>`'s.

    Returns:
        A valid TikZ command.
    """
    params = f"[{', '.join(p.tikz() for p in args)}]" if args else ""
    return rf"\{name}{params} {body};"


def svg_command(name: str, *args: POProperty) -> str:
    """
    Put together an SVG command from its components.

    Parameters:
        name: Name of the command, that is, `<{name}>`.
        *args: Parameters of the command, which correspond to key-value pairs
            when compiled, but are given as :class:`POProperty<pythagoras.pobject.POProperty>`'s.

    Returns:
        A valid SVG command.
    """
    params = " ".join(p.svg() for p in args) if args else ""
    return rf"<{name} {params} />"


def svg_path(points: Iterable[tuple[float, float]], *args: POProperty) -> str:
    """
    Construct an SVG path from its points.

    Parameters:
        points: The sequence of points (in the SVG coordinate system) that make up the path.

    Returns:
        Final `<path d="...">` tag.
    """
    iterator = iter(points)
    p0 = next(iterator)
    path = f"M {p0[0]:.4f} {p0[1]:.4f}"
    for p in iterator:
        path += f" L {p[0]:.4f} {p[1]:.4f}"
    return svg_command("path", CustomStyle("d", path), *args)


def fill_default_args(
    args: Iterable[POProperty], *defaults: tuple[type, POProperty]
) -> list[POProperty]:
    """
    Complete a list of :class:`POProperty<pythagoras.pobject.POProperty>`'s with default values for the types that are missing.

    Parameters:
        args: Initial set of properties.
        defaults: List of types with their default values.

    Returns:
        The completion of `args`.
    """
    xs = list(args)
    for q, e in defaults:
        if not any(isinstance(x, q) for x in args):
            xs.append(e)
    return xs


class RasterPicture:
    """
    Wrapper class for raster images; contains a grid to which 2D shapes can be drawn
    via the methods implemented herein.

    Attributes:
        context: Attributes of the picture (height, width, scaling, ...).
        data: Matrix containing the rasterized pixels as :class:`pythagoras.style.color.Color`
            instances.
    """

    __context: RenderingContext
    __data: list[list[Color]]

    def __init__(self, ctx: RenderingContext) -> None:
        self.__context = ctx
        self.clear()

    def clear(self) -> None:
        """Erases the current picture and fills it with white pixels."""
        self.__data = [
            [Color(255, 255, 255) for _ in range(ceil(self.__context.width))]
            for _ in range(ceil(self.__context.height))
        ]

    @property
    def context(self) -> RenderingContext:
        return self.__context

    @context.setter
    def context(self, ctx: RenderingContext) -> None:
        self.__context = ctx
        self.clear()

    @property
    def data(self) -> list[list[Color]]:
        return self.__data

    def draw_pixel(self, x: int, y: int, color: Color, opacity: float) -> None:
        """
        Fills a pixel of the picture.

        Parameters:
            x: :math:`x`-coordinate of the pixel.
            y: :math:`y`-coordinate of the pixel.
            color: Color of the pixel.
            opacity: Opacity.
        """
        if x < 0 or x > self.__context.width:
            return
        if y < 0 or y > self.__context.height:
            return
        self.__data[y][x] = (color - self.__data[y][x]) * opacity + self.__data[y][x]

    def draw_stamp(self, x: int, y: int, r: int, color: Color, opacity: float) -> None:
        """
        Paints a very simple filled circle.

        Parameters:
            x: :math:`x`-coordinate of the center.
            y: :math:`y`-coordinate of the center.
            r: Radius of the circle.
            color: Color of the circle.
            opacity: Opacity.
        """
        for i in range(-r, r + 1):
            for j in range(-r, r + 1):
                if i * i + j * j <= r * r:
                    self.draw_pixel(x + i, y + j, color, opacity)

    def draw_segment(
        self, a: tuple[float, float], b: tuple[float, float], *args: POProperty
    ) -> None:
        """
        Draws the segment that joins two points to the image data, using Bresenham's line algorithm.

        Parameters:
            a: First point, expressed in Cartesian coordinates.
            b: Second point, expressed in Cartesian coordinates.
            args: Styles to be applied to the line; only :class:`pythagoras.style.draw.LineWidth`,
                :class:`pythagoras.style.draw.Stroke`, :class:`pythagoras.style.opacity.Opacity`,
                and :class:`pythagoras.style.draw.StrokeOpacity` apply here.
        """
        h, w, s, (ox, oy) = (
            self.__context.height,
            self.__context.width,
            self.__context.scale,
            self.__context.origin,
        )
        ax = round(w / 2 + (a[0] - ox) * s)
        ay = round(h / 2 - (a[1] - oy) * s)
        bx = round(w / 2 + (b[0] - ox) * s)
        by = round(h / 2 - (b[1] - oy) * s)

        stroke = Color(0, 0, 0)
        width = 1
        opacity = 1.0

        for t in args:
            if isinstance(t, Stroke):
                stroke = t.color if t.color else stroke
            elif isinstance(t, LineWidth):
                width = t.width
            elif isinstance(t, (Opacity, StrokeOpacity)):
                opacity = t.opacity

        dx, sx = abs(ax - bx), 1 if ax < bx else -1
        dy, sy = -abs(ay - by), 1 if ay < by else -1
        e = dx + dy

        while True:
            if width == 1:
                self.draw_pixel(ax, ay, stroke, opacity)
            else:
                self.draw_stamp(ax, ay, int(width / 2), stroke, opacity)

            if (e2 := 2 * e) >= dy:
                if ax == bx:
                    break
                e += dy
                ax += sx
            if e2 <= dx:
                if ay == by:
                    break
                e += dx
                ay += sy
