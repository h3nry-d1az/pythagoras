from collections.abc import Iterable

from .pobject import PObject, POProperty

__all__ = ["Canvas"]


class Canvas:
    """
    Container class for a collection of :class:`PObject <pythagoras.pobject.PObject>`'s. Controls the SVG and TikZ output,
    and resizes automatically when a new element is added.

    Attributes:
        scale: The scaling factor by which the canvas is stretched. When exporting to TikZ,
               this is compiled exactly into `[scale={scale}]`, and when using SVG, the
               distances are muliplied by its value.
    """

    scale: float
    _xmin: float
    _xmax: float
    _ymin: float
    _ymax: float
    _yrange: list[float]
    __elements: list[tuple[PObject, tuple[POProperty, ...]]]

    def __init__(self, scale: float = 1) -> None:
        self.scale = scale
        self._xmin = 0
        self._xmax = 0
        self._ymin = 0
        self._ymax = 0
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
            p = (p[0] * self.scale, p[1] * self.scale)
            self._xmin = min(p[0], self._xmin)
            self._xmax = max(p[0], self._xmax)
            self._ymin = min(p[1], self._ymin)
            self._ymax = max(p[1], self._ymax)
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
        return (
            r"\documentclass[crop,tikz]{standalone}"
            + "\n"
            + r"\begin{document}"
            + "\n"
            + r"\begin{tikzpicture}"
            + (f"[scale={self.scale}]" if self.scale != 1 else "")
            + "\n"
            + "\n".join(e.tikz(*a) for e, a in sorted(self.__elements))
            + "\n"
            + r"\end{tikzpicture}"
            + "\n"
            + r"\end{document}"
        )

    def svg(self) -> str:
        """
        Render the scene into SVG.

        Returns:
            The final SVG picture.
        """
        width = self._xmax - self._xmin + 5
        height = self._ymax - self._ymin + 5
        O = ((self._xmax + self._xmin) / 2, (self._ymax + self._ymin) / 2)
        return (
            f'<svg width="{width:.4f}" height="{height:.4f}" xmlns="http://www.w3.org/2000/svg">\n'
            + "\n".join(
                e.svg(O, width, height, self.scale, *a)
                for e, a in sorted(self.__elements)
            )
            + "\n"
            + "</svg>"
        )
