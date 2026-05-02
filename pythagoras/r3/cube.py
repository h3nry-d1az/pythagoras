from dataclasses import dataclass

from ..backend import fill_default_args, svg_path, tikz_command
from ..pobject import POProperty
from ..style.color import BLACK
from ..style.draw import Fill, Stroke
from ..utils import cartesian_to_canvas
from .camera import Camera3D
from .pobject import PObject3D
from .rendering import project_point

__all__ = ["Cube"]


@dataclass
class Cube(PObject3D):
    """
    Cube that cannot be rotated.

    Attributes:
        center: Center of the cube.
        side: Length of its side.
    """

    center: tuple[float, float, float]
    side: float

    @property
    def vertices(
        self,
    ) -> tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ]:
        """Vertices of the cube."""
        return (
            (
                self.center[0] + self.side / 2,
                self.center[1] + self.side / 2,
                self.center[2] + self.side / 2,
            ),
            (
                self.center[0] + self.side / 2,
                self.center[1] + self.side / 2,
                self.center[2] - self.side / 2,
            ),
            (
                self.center[0] + self.side / 2,
                self.center[1] - self.side / 2,
                self.center[2] + self.side / 2,
            ),
            (
                self.center[0] + self.side / 2,
                self.center[1] - self.side / 2,
                self.center[2] - self.side / 2,
            ),
            (
                self.center[0] - self.side / 2,
                self.center[1] + self.side / 2,
                self.center[2] + self.side / 2,
            ),
            (
                self.center[0] - self.side / 2,
                self.center[1] + self.side / 2,
                self.center[2] - self.side / 2,
            ),
            (
                self.center[0] - self.side / 2,
                self.center[1] - self.side / 2,
                self.center[2] + self.side / 2,
            ),
            (
                self.center[0] - self.side / 2,
                self.center[1] - self.side / 2,
                self.center[2] - self.side / 2,
            ),
        )

    def svg(
        self,
        camera: Camera3D,
        frustum: float,
        width: float,
        height: float,
        scale: float,
        *args: POProperty,
    ) -> str:
        ps = (project_point(camera, frustum, p) for p in self.vertices)
        return svg_path(
            (cartesian_to_canvas(*p, width, height, scale) for p in ps if p),
            (0, 0),
            width,
            height,
            scale,
            *fill_default_args(args, (Fill, Fill(None)), (Stroke, Stroke(BLACK))),
        )

    def tikz(self, camera: Camera3D, frustum: float, *args: POProperty) -> str:
        ps = (project_point(camera, frustum, p) for p in self.vertices)
        return tikz_command(
            "draw", " -- ".join(f"({p[0]}, {p[1]})" for p in ps if p), *args
        )
