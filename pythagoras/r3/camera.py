from dataclasses import dataclass

__all__ = ["Camera3D"]


@dataclass
class Camera3D:
    """
    Camera which encodes the position and direction of the rendering frame of reference.

    Attributes:
        x: :math:`x`-coordinate of the position.
        y: :math:`y`-coordinate of the position.
        z: :math:`z`-coordinate of the position.
        x: :math:`x` component of the unit vector pointing in the direction of view.
        y: :math:`y` component of the unit vector pointing in the direction of view.
        z: :math:`z` component of the unit vector pointing in the direction of view.
    """

    x: float
    y: float
    z: float
    px: float = 1
    py: float = 0
    pz: float = 0
