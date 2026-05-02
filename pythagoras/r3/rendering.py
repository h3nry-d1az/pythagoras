from math import cos, sin

from .camera import Camera3D
from .vector import Vector3D

__all__ = ["project_point"]


def project_point(
    camera: Camera3D, frustum: float, point: tuple[float, float, float]
) -> tuple[float, float] | None:
    r"""
    Projects a point in :math:`\mathbf R^3` *with perspective* onto the plane centered
    at the position of the camera, and having its pointing vector as the normal vector of the plane.

    Parameters:
        camera: :class:`Camera3D <pythagoras.r3.camera.Camera3D>` object encoding the plane.
        frustum: Field of view.
        point: Point to be projected.

    Returns:
        The projected point or `None` if it is behind the camera.
    """
    w = Vector3D(*camera.direction)
    u = Vector3D(1, 0, 0) if w() == (0, 1, 0) else Vector3D(0, 1, 0) ^ w
    u /= abs(u)
    v = w ^ u
    u, v = (
        cos(camera.theta) * u + sin(camera.theta) * v,
        -sin(camera.theta) * u + cos(camera.theta) * v,
    )
    p = Vector3D.from_two_points(camera.position, point)
    x, y, z = p @ u, p @ v, p @ w
    if z <= 0:
        return None
    return (x * frustum / z, y * frustum / z)
