from dataclasses import dataclass

from ..backend import fill_default_args, svg_command, tikz_command
from ..pobject import POProperty
from ..style import CustomStyle
from ..style.color import BLACK
from ..style.draw import Fill, LineWidth, Stroke
from ..utils import cartesian_to_canvas
from .camera import Camera3D
from .pobject import PObject3D
from .rendering import project_point

__all__ = ["FakeSphere"]


@dataclass(init=False)
class FakeSphere(PObject3D):
    r"""
    Circle centered in a point in :math:`\mathbf R^3` which emulates a sphere.

    Attributes:
        center: Center of the fake sphere.
        radius: Radius of the fake sphere.
    """

    center: tuple[float, float, float]
    radius: float

    def __init__(
        self, center: tuple[float, float, float], radius: float, zord: int = 0
    ) -> None:
        self.center = center
        self.radius = radius
        self._zord = zord

    def visible_radius(self, camera: Camera3D, frustum: float) -> float:
        """
        Compute the radius of the sphere from the perspective of the camera.

        Returns:
            Radius from that angle.
        """
        return self.radius * frustum / (self.center[2] - camera.position[2])

    def svg(
        self,
        camera: Camera3D,
        frustum: float,
        width: float,
        height: float,
        scale: float,
        *args: POProperty,
    ) -> str:
        _pc = project_point(camera, frustum, self.center)
        if not _pc:
            return ""
        cx, cy = cartesian_to_canvas(*_pc, width, height, scale)
        vr = self.visible_radius(camera, frustum) * scale
        args = (
            CustomStyle("cx", cx),
            CustomStyle("cy", cy),
            CustomStyle("r", vr),
            *args,
        )
        return svg_command(
            "circle",
            *fill_default_args(
                args,
                (Fill, Fill(None)),
                (Stroke, Stroke(BLACK)),
                (LineWidth, LineWidth(vr / 20)),
            ),
        )

    def tikz(self, camera: Camera3D, frustum: float, *args: POProperty) -> str:
        p = project_point(camera, frustum, self.center)
        if not p:
            return ""
        cmd = "filldraw" if any(isinstance(x, Fill) for x in args) else "draw"
        return tikz_command(
            cmd,
            f"({p[0]}, {p[1]}) circle ({self.visible_radius(camera, frustum)})",
            *args,
        )
