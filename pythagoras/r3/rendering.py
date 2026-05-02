from .camera import Camera3D

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
    pass
