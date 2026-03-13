from heapq import heapify, heappush

from .pobject import PObject


class Canvas:
    height: int
    width: int
    __elements: list[PObject]

    def __init__(self, height: int, width: int, *args: PObject) -> None:
        self.height = height
        self.width = width
        self.__elements = list(args)
        heapify(self.__elements)

    def add(self, *args: PObject) -> None:
        for obj in args:
            heappush(self.__elements, obj)

    def tikz(self) -> str:
        return (
            r"\documentclass[crop,tikz]{standalone}"
            + "\n"
            + r"\begin{document}"
            + "\n"
            + r"\begin{tikzpicture}"
            + "\n"
            + "\n".join(e.tikz() for e in self.__elements)
            + "\n"
            + r"\end{tikzpicture}"
            + "\n"
            + r"\end{document}"
        )

    def svg(self) -> str:
        return (
            f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">\n'
            + "\n".join(e.svg() for e in self.__elements)
            + "\n"
            + "</svg>"
        )
