from math import atan2, cos, degrees, pi, sin

from .backend import fill_default_args, svg_command, tikz_command
from .pobject import PObject, POProperty
from .style import CustomProperty, CustomStyle, color
from .style.draw import Fill, Stroke
from .utils import cartesian_to_canvas

__all__ = ["Arrow"]


class Arrow(PObject):
    """
    A pointing arrow in space; it may possibly represent a vector.

    Attributes:
        start: Point from which the arrow emanates.
        end: Point at which the head is located.
        size: Size of the arrowhead.
        width: Flare angle of the arrowhead.
    """

    start: tuple[float, float]
    end: tuple[float, float]
    size: float
    angle: float

    def __init__(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        size: float = 1,
        angle: float = pi / 12,
        zord: int = 0,
    ) -> None:
        self.start = start
        self.end = end
        self.size = size
        self.angle = angle
        self._zord = zord

    def extrema(self) -> list[tuple[float, float]]:
        return [self.start, self.end, *self.make_arrowhead()]

    def make_arrowhead(self) -> tuple[tuple[float, float], tuple[float, float]]:
        """
        Computes the points which make up the arrowhead.

        Returns:
            The left- and rightmost points of the arrowhead.
        """
        alpha = atan2(self.end[1] - self.start[1], self.end[0] - self.start[0])
        return (
            (
                self.end[0] - self.size * cos(alpha - self.angle),
                self.end[1] - self.size * sin(alpha - self.angle),
            ),
            (
                self.end[0] - self.size * cos(alpha + self.angle),
                self.end[1] - self.size * sin(alpha + self.angle),
            ),
        )

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: POProperty,
    ) -> str:
        x1, y1 = cartesian_to_canvas(*self.start, width, height, scale)
        x2, y2 = cartesian_to_canvas(*self.end, width, height, scale)
        left, right = self.make_arrowhead()
        lx, ly = cartesian_to_canvas(*left, width, height, scale)
        rx, ry = cartesian_to_canvas(*right, width, height, scale)
        x1 -= origin[0]
        y1 += origin[1]
        x2 -= origin[0]
        y2 += origin[1]
        lx -= origin[0]
        ly += origin[1]
        rx -= origin[0]
        ry += origin[1]
        return "\n".join(
            (
                svg_command(
                    "line",
                    CustomStyle("x1", x1),
                    CustomStyle("y1", y1),
                    CustomStyle("x2", x2),
                    CustomStyle("y2", y2),
                    *args,
                ),
                svg_command(
                    "polygon",
                    CustomStyle("points", f"{x2},{y2} {lx},{ly} {rx},{ry}"),
                    *fill_default_args(
                        args, (Fill, Fill(color.WHITE)), (Stroke, Stroke(color.BLACK))
                    ),
                ),
            )
        )

    def tikz(self, *args: POProperty) -> str:
        return tikz_command(
            r"\draw",
            f"{self.start} -- {self.end}",
            CustomProperty(
                f"-{{Straight Barb[angle={degrees(self.angle)}, length={self.size}bp]}}"
            ),
        )
