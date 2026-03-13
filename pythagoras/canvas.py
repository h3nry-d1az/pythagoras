from heapq import heapify, heappush

from .pobject import PObject, POProperty


class Canvas:
    height: float
    width: float
    scale: float
    __elements: list[tuple[PObject, tuple[str, ...], dict[str, POProperty]]]

    def __init__(self, width: float, height: float, *args: PObject) -> None:
        self.height = height
        self.width = width
        self.scale = 1
        self.__elements = []
        heapify(self.__elements)

    def add(self, obj: PObject, *args: str, **kwargs: POProperty) -> None:
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
        return (
            f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">\n'
            + "\n".join(
                e.svg(self.width, self.height, self.scale, *a, **k)
                for e, a, k in self.__elements
            )
            + "\n"
            + "</svg>"
        )
