from collections.abc import Iterable

from .pobject import PObject, POProperty, RenderingContext

__all__ = ["Canvas"]


class Canvas:
    """
    Container class for a collection of :class:`PObject <pythagoras.pobject.PObject>`'s.
    Controls the SVG and TikZ output, and resizes automatically when a new element is added.

    Attributes:
        context: State of the canvas; groups its scaling, its bounding box, and so forth. It
            can be queried to retrieve its current height, origin, etc.
    """

    context: RenderingContext
    __elements: list[tuple[PObject, tuple[POProperty, ...]]]

    def __init__(self, scale: float = 1) -> None:
        self.context = RenderingContext(scale, 0, 0, 0, 0)
        self.__elements = []

    def add(self, obj: PObject, *args: POProperty) -> None:
        """
        Appends an element into the list of objects to be renderded.

        Parameters:
            obj: :class:`PObject <pythagoras.pobject.PObject>` to be included into the scene.
            *args: Parameters of the object, i.e.: `Fill(BLUE)` or `Stroke(RED)`. See :mod:`pythagoras.style` for
                further information on styling.
        """
        for p in obj.extrema():
            self.context.xmin = min(p[0], self.context.xmin)
            self.context.xmax = max(p[0], self.context.xmax)
            self.context.ymin = min(p[1], self.context.ymin)
            self.context.ymax = max(p[1], self.context.ymax)
        self.__elements.append((obj, args))

    def add_many(self, objs: Iterable[PObject], *args: POProperty) -> None:
        """
        Appends a collection of elements sharing common arguments into the list of objects to be renderded.

        Parameters:
            objs: Sequence of :class:`PObject <pythagoras.pobject.PObject>`'s to be included into the scene.
            *args: Parameters of the object, i.e.: `Fill(BLUE)` or `Stroke(RED)`. See :mod:`pythagoras.style` for
                further information on styling.
        """
        for obj in objs:
            self.add(obj, *args)

    def tikz(self) -> str:
        """
        Render the scene into TikZ.

        Returns:
            The compiled TikZ document.
        """
        return "\n".join(
            (
                r"\documentclass[crop,tikz]{standalone}",
                r"\usetikzlibrary{arrows.meta}"
                r"\begin{document}",
                r"\begin{tikzpicture}"
                + (f"[scale={self.context.scale}]" if self.context.scale != 1 else ""),
                "\n".join(e.tikz(self.context, *a) for e, a in sorted(self.__elements)),
                r"\end{tikzpicture}",
                r"\end{document}",
            )
        )

    def svg(self) -> str:
        """
        Render the scene into SVG.

        Returns:
            The final SVG picture.
        """
        return "\n".join(
            (
                f'<svg width="{self.context.width:.4f}" height="{self.context.height:.4f}" '
                'xmlns="http://www.w3.org/2000/svg">',
                "\n".join(e.svg(self.context, *a) for e, a in sorted(self.__elements)),
                "</svg>",
            )
        )

    @property
    def scale(self) -> float:
        """
        Scaling factor stored in the `context` attribute.
        """
        return self.context.scale

    @scale.setter
    def scale(self, scale: float) -> None:
        """
        Gives a value to the scaling factor in `context`.
        """
        self.context.scale = scale
