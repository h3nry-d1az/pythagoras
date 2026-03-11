from .pobject import PObject, POProperties
from typing_extensions import Unpack
from typing import Self

class Circle(PObject):
    x: float
    y: float
    radius: float
    __fill: bool

    def __init__(
        self,
        x: float,
        y: float,
        radius: float = 2.,
        zord: int = 0,
        *args: str,
        **kwargs: Unpack[POProperties]
    ) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self._zord = zord
        self._args = list(args)
        self._kwargs = list(kwargs.items())
        if "color" not in kwargs:
            self._kwargs.append(("color", "black"))
        self.__fill = "fill" in kwargs.keys()

    @property
    def tikz(self) -> str:
        return fr"{r'\filldraw' if self.__fill else r'\draw'}"\
               fr"[{', '.join(f'{n}={v}' for n, v in self._kwargs) + ', '.join(self._args)}]"\
               fr"({self.x}, {self.y}) circle ({self.radius});"

    @property
    def pstricks(self) -> str:
        return fr"\psdot[dotsize={self.radius}, {', '.join(f'{n}={v}' for n, v in self._kwargs) + ', '.join(self._args)}]({self.x}, {self.y})"

    @property
    def svg(self) -> str:
        return fr'<circle cx="{self.x}" cy="{self.y}" r="{self.radius}" '\
            fr'{' '.join(f'{n}="{v}"' for n, v in self._kwargs) + ' '.join(self._args)}/>'

    @classmethod
    def from_three_points(cls, p1: tuple[int, int], p2: tuple[int, int], p3: tuple[int, int]) -> Self:
        return cls(0, 0, name='', value=0)