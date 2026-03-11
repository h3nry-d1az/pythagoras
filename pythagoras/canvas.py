from .pobject import PObject
from heapq import heapify, heappush

class Canvas(object):
    elements: list[PObject]

    def __init__(self, *args: PObject) -> None:
        self.elements = list(args)
        heapify(self.elements)

    def add(self, *args: PObject) -> None:
        for obj in args:
            heappush(self.elements, obj)

    @property
    def tikz(self) -> str:
        return "\n".join(map(lambda e: e.tikz, self.elements))

    @property
    def tikz_doc(self) -> str:
        return r"\documentclass[crop,tikz]{standalone}"+'\n'\
             + r"\begin{document}"+'\n'\
             + r"\begin{tikzpicture}"+'\n'\
             + f"{self.tikz}\n"\
             + r"\end{tikzpicture}"+'\n'\
             + r"\end{document}"+'\n'

    @property
    def pstricks(self) -> str:
        return "\n".join(map(lambda e: e.pstricks, self.elements))

    @property
    def svg(self) -> str:
        return "\n".join(map(lambda e: e.svg, self.elements))