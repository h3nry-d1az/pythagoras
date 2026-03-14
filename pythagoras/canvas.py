from heapq import heapify, heappush

from .pobject import PObject, POProperty

__all__ = ["Canvas"]


class Canvas:
    scale: float
    _xmin: float
    _xmax: float
    _ymin: float
    _ymax: float
    _yrange: list[float]
    __elements: list[tuple[PObject, tuple[str, ...], dict[str, POProperty]]]

    def __init__(self) -> None:
        self.scale = 1
        self._xmin = 0
        self._xmax = 0
        self._ymin = 0
        self._ymax = 0
        self.__elements = []
        heapify(self.__elements)

    def add(self, obj: PObject, *args: str, **kwargs: POProperty) -> None:
        for p in obj.extrema():
            p = (p[0] * self.scale, p[1] * self.scale)
            self._xmin = min(p[0], self._xmin)
            self._xmax = max(p[0], self._xmax)
            self._ymin = min(p[1], self._ymin)
            self._ymax = max(p[1], self._ymax)
        heappush(self.__elements, (obj, args, kwargs))

    def tikz(self) -> str:
        return (
            r"\documentclass[crop,tikz]{standalone}"
            + "\n"
            + r"\begin{document}"
            + "\n"
            + r"\begin{tikzpicture}"
            + (f"[scale={self.scale}]" if self.scale != 1 else "")
            + "\n"
            + "\n".join(e.tikz(*a, **k) for e, a, k in self.__elements)
            + "\n"
            + r"\end{tikzpicture}"
            + "\n"
            + r"\end{document}"
        )

    def svg(self) -> str:
        width = self._xmax - self._xmin + 5
        height = self._ymax - self._ymin + 5
        O = ((self._xmax + self._xmin) / 2, (self._ymax + self._ymin) / 2)
        return (
            f'<svg width="{width:.4f}" height="{height:.4f}" xmlns="http://www.w3.org/2000/svg">\n'
            + "\n".join(
                e.svg(O, width, height, self.scale, *a, **k)
                for e, a, k in self.__elements
            )
            + "\n"
            + "</svg>"
        )
