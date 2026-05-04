from collections.abc import Iterable

from ..pobject import PObject, POProperty, RenderingContext
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
        origin: Point in 2D space to which the origin of the frame of reference corresponds.
        camera: :class:`Camera3D <pythagoras.r3.camera.Camera3D>` object encoding the position
            and pointing direction of the rendering camera.
        frustum: Field of view within the scene.
        scale: The scaling factor by which the canvas is stretched.
    """

    dimensions: tuple[float, float]
    origin: tuple[float, float]
    camera: Camera3D
    frustum: float
    scale: float
    __elements: list[tuple[PObject3D, tuple[POProperty, ...]]]
    __light_sources: list[tuple[tuple[float, float, float], float]]
    __camera_light: bool

    def __init__(
        self,
        dimensions: tuple[float, float],
        origin: tuple[float, float] = (0, 0),
        camera: Camera3D | None = None,
        frustum: float = 1,
        scale: float = 1,
    ) -> None:
        self.dimensions = dimensions
        self.origin = origin
        self.camera = camera if camera else Camera3D((0, 0, 0))
        self.scale = scale
        self.frustum = frustum
        self.__elements = []
        self.__light_sources = []
        self.__camera_light = True

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

    def add_light_source(
        self, position: tuple[float, float, float], intensity: float
    ) -> None:
        """
        Includes a light source into the scene.
        By default, the camera emmits light with an intensity equal to the frustum;
        this behavior may be changed through the :meth:`camera_as_light_source` property.

        Parameters:
            position: Position of the light source.
            intensity: Its brightness.
        """
        self.__light_sources.append((position, intensity))

    @property
    def camera_as_light_source(self) -> bool:
        """
        Returns `True` if the camera is acting as a light source, `False` otherwise.
        """
        return self.__camera_light

    @camera_as_light_source.setter
    def camera_as_light_source(self, value: bool) -> None:
        """
        Changes whether the camera should act as a light source.
        """
        self.__camera_light = value

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

    def svg(self, ctx: RenderingContext, *args: POProperty) -> str:
        cx, cy = cartesian_to_canvas(
            (
                self.origin[0] - self.dimensions[0] / 2,
                self.origin[1] + self.dimensions[1] / 2,
            ),
            ctx,
        )
        return (
            f'<svg x="{cx}" y="{cy}" width="{self.dimensions[0] * ctx.scale}" height="{self.dimensions[1] * ctx.scale}" '
            f'viewBox="0 0 {self.dimensions[0]} {self.dimensions[1]}">\n'
            + "\n".join(
                e[0].svg(
                    self.camera,
                    self.frustum,
                    *self.dimensions,
                    self.scale,
                    [*self.__light_sources, (self.camera.position, self.frustum)]
                    if self.camera_as_light_source
                    else self.__light_sources,
                    *e[1],
                    *args,
                )
                for e in sorted(self.__elements)
            )
            + "\n</svg>"
        )

    def tikz(self, ctx: RenderingContext, *args: POProperty) -> str:
        return "\n".join(
            [
                rf"\begin{{scope}}[shift={{({self.origin[0] - self.dimensions[0] / 2}, {self.origin[1] - self.dimensions[1] / 2})}}, scale={self.scale:.4f}]",
                rf"\clip ({-self.dimensions[0] / 2}, {-self.dimensions[1] / 2}) rectangle ({self.dimensions[0] / 2}, {self.dimensions[1] / 2});",
                *(
                    e[0].tikz(
                        self.camera,
                        self.frustum,
                        [*self.__light_sources, (self.camera.position, self.frustum)]
                        if self.camera_as_light_source
                        else self.__light_sources,
                        *e[1],
                        *args,
                    )
                    for e in sorted(self.__elements)
                ),
                r"\end{scope}",
            ]
        )
