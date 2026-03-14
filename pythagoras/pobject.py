from abc import ABC, abstractmethod
from typing import Self

__all__ = ["POProperty", "PObject"]

POProperty = str | float


class PObject(ABC):
    _zord: int

    def __lt__(self, other: Self):
        return self._zord < other._zord

    @abstractmethod
    def extrema(self) -> list[tuple[float, float]]:
        pass

    @abstractmethod
    def tikz(self, *args: str, **kwargs: POProperty) -> str:
        pass

    @abstractmethod
    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: str,
        **kwargs: POProperty,
    ) -> str:
        pass
