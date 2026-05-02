from collections.abc import Iterable

from ..pobject import PObject, POProperty
from ..utils import cartesian_to_canvas
from .camera import Camera3D
from .pobject import PObject3D

__all__ = ["Canvas3D"]


class Canvas3D(PObject):
    """
    Container for a collection of :class:`PObject3D <pythagoras.r3.pobject.PObject3D>`'s.
    Controls the SVG and TikZ output for the entire 3D scene.

    Attributes:
        dimensions: Width and height of the canvas.
        camera: :class:`Camera3D <pythagoras.r3.camera.Camera3D>` object encoding the position
            and pointing direction of the rendering camera.
        origin: Point in 2D space to which the origin of the frame of reference corresponds.
        scale: The scaling factor by which the canvas is stretched.
        frustum: Field of view within the scene.
    """

    dimensions: tuple[float, float]
    origin: tuple[float, float]
    camera: Camera3D
    scale: float
    frustum: float
    __elements: list[tuple[PObject3D, tuple[POProperty, ...]]]

    def __init__(
        self,
        dimensions: tuple[float, float],
        origin: tuple[float, float] = (0, 0),
        camera: Camera3D | None = None,
        scale: float = 1,
        frustum: float = 1,
    ) -> None:
        self.dimensions = dimensions
        self.origin = origin
        self.camera = camera if camera else Camera3D((0, 0, 0))
        self.scale = scale
        self.frustum = frustum
        self.__elements = []

    def add(self, obj: PObject3D, *args: POProperty) -> None:
        """
        Appends a 3D object together with its properties into the list of elements to be renderded.

        Parameters:
            obj: :class:`PObject3D <pythagoras.r3.pobject.PObject3D>` to be included into the scene.
            *args: Parameters of the object, i.e.: `Fill(BLUE)` or `Stroke(RED)`. See :mod:`pythagoras.style` for
                further information on styling.
        """
        self.__elements.append((obj, args))

    def add_many(self, objs: Iterable[PObject3D], *args: POProperty) -> None:
        """
        Appends a collection of 3D objects sharing common arguments into the list of elements to be renderded.

        Parameters:
            objs: Sequence of :class:`PObject3D <pythagoras.r3.pobject.PObject3D>`'s to be included into the scene.
            *args: Parameters of the object, i.e.: `Fill(BLUE)` or `Stroke(RED)`. See :mod:`pythagoras.style` for
                further information on styling.
        """
        for obj in objs:
            self.add(obj, *args)

    def extrema(self) -> list[tuple[float, float]]:
        return [
            (
                self.origin[0] - self.dimensions[0] / 2,
                self.origin[1] - self.dimensions[1] / 2,
            ),
            (
                self.origin[0] + self.dimensions[0] / 2,
                self.origin[1] + self.dimensions[1] / 2,
            ),
        ]

    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: POProperty,
    ) -> str:
        cx, cy = cartesian_to_canvas(
            self.origin[0] - scale * self.dimensions[0] / 2,
            self.origin[1] + scale * self.dimensions[1] / 2,
            width,
            height,
            scale,
        )
        return (
            f'<svg x="{cx}" y="{cy}" width="{self.dimensions[0] * scale}" height="{self.dimensions[1] * scale}" viewBox="0 0 {self.dimensions[0]} {self.dimensions[1]}">\n'
            + "\n".join(
                e[0].svg(self.camera, self.frustum, *self.dimensions, self.scale, *e[1])
                for e in sorted(self.__elements)
            )
            + "\n</svg>"
        )

    def tikz(self, *args: POProperty) -> str:
        return "\n".join(
            [
                rf"\begin{{scope}}[shift={{({self.origin[0] - self.dimensions[0] / 2}, {self.origin[1] - self.dimensions[1] / 2})}}, scale={self.scale:.4f}]",
                rf"\clip (0, 0) rectangle ({self.dimensions[0]}, {self.dimensions[1]});",
                *(
                    e[0].tikz(self.camera, self.frustum, *e[1])
                    for e in sorted(self.__elements)
                ),
                r"\end{scope}",
            ]
        )
