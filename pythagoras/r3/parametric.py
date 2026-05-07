from collections.abc import Callable

from ..backend import fill_default_args, svg_path, tikz_command
from ..pobject import POProperty, RenderingContext
from ..style.color import BLACK
from ..style.draw import Fill, LineWidth, Stroke
from ..utils import cartesian_to_canvas
from .camera import Camera3D
from .pobject import PObject3D
from .rendering import project_point

__all__ = ["Trajectory"]


class Trajectory(PObject3D):
    r"""
    Curve in :math:`\mathbf R^3` traced by a single-variable parametric function.

    Attributes:
        phi: The function which determines the shape.
        a: Start of the time domain.
        b: End of the time domain.
        dt: Increment in time between each point. If it is less than or equal
            to zero, the time domain will be split into 100 intervals.
    """

    phi: Callable[[float], tuple[float, float, float]]
    a: float
    b: float
    dt: float

    def __init__(
        self,
        phi: Callable[[float], tuple[float, float, float]],
        a: float,
        b: float,
        dt: float = 0,
        zord: int = 0,
    ) -> None:
        self.phi = phi
        self.a = a
        self.b = b
        self.dt = dt if dt > 0 else (b - a) / 100
        self._zord = zord

    def make_points(self) -> list[tuple[float, float, float]]:
        """
        Compute the positions of each of the samples of the curve.

        Returns:
            List containing the sampled points.
        """
        ps: list[tuple[float, float, float]] = []
        t = self.a
        while t <= self.b:
            t += self.dt
            ps.append(self.phi(t))
        return ps

    def svg(
        self,
        camera: Camera3D,
        frustum: float,
        width: float,
        height: float,
        scale: float,
        lights: list[tuple[tuple[float, float, float], float]],
        *args: POProperty,
    ) -> str:
        ctx = RenderingContext.from_dimensions(scale, width, height)
        ps = (
            cartesian_to_canvas(p, ctx)
            for p in (project_point(camera, frustum, pp) for pp in self.make_points())
            if p
        )
        return svg_path(
            ps,
            *fill_default_args(
                args,
                (Fill, Fill(None)),
                (Stroke, Stroke(BLACK)),
                (LineWidth, LineWidth(0.01)),
            ),
        )

    def tikz(
        self,
        camera: Camera3D,
        frustum: float,
        lights: list[tuple[tuple[float, float, float], float]],
        *args: POProperty,
    ) -> str:
        return tikz_command(
            "draw",
            " -- ".join(
                str(project_point(camera, frustum, p)) for p in self.make_points()
            ),
        )
