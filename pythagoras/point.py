from .pobject import PObject, POProperties
from typing_extensions import Unpack

class Point(PObject):
    x: float
    y: float
    _radius: float

    def __init__(
        self,
        x: float,
        y: float,
        _radius: float = 2.,
        zord: int = 0,
        *args: str,
        **kwargs: Unpack[POProperties]
    ) -> None:
        self.x = x
        self.y = y
        self._radius = _radius
        self._zord = zord
        self._args = list(args)
        self._kwargs = list(kwargs.items())
        if "color" not in kwargs:
            self._kwargs.append(("color", "black"))
        if "fill" not in kwargs:
            self._kwargs.append(("fill", "white"))

    @property
    def tikz(self) -> str:
        return fr"\filldraw[{', '.join(f'{n}={v}' for n, v in self._kwargs) + ', '.join(self._args)}]"\
               fr"({self.x}, {self.y}) circle ({self._radius});"

    @property
    def pstricks(self) -> str:
        return fr"\psdot[dotsize={self._radius}, {', '.join(f'{n}={v}' for n, v in self._kwargs) + ', '.join(self._args)}]({self.x}, {self.y})"

    @property
    def svg(self) -> str:
        return fr'<circle cx="{self.x}" cy="{self.y}" r="{self._radius}" '\
            fr'{' '.join(f'{n}="{v}"' for n, v in self._kwargs) + ' '.join(self._args)}/>'