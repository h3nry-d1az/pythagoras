from dataclasses import dataclass
from math import hypot

__all__ = ["Camera3D"]


@dataclass(init=False)
class Camera3D:
    """
    Camera which encodes the position and direction of the rendering frame of reference.

    Attributes:
        x: :math:`x`-coordinate of the position.
        y: :math:`y`-coordinate of the position.
        z: :math:`z`-coordinate of the position.
        px: :math:`x` component of the unit vector pointing in the direction of view.
        py: :math:`y` component of the unit vector pointing in the direction of view.
        pz: :math:`z` component of the unit vector pointing in the direction of view.
        theta: Rotation of the camera.
    """

    x: float
    y: float
    z: float
    px: float
    py: float
    pz: float
    theta: float

    def __init__(
        self,
        c: tuple[float, float, float],
        p: tuple[float, float, float] = (0, 0, 1),
        theta: float = 0,
    ) -> None:
        self.x, self.y, self.z = c
        self.px, self.py, self.pz = (t / hypot(*p) for t in p)
        self.theta = theta

    @property
    def position(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)

    @property
    def direction(self) -> tuple[float, float, float]:
        return (self.px, self.py, self.pz)
