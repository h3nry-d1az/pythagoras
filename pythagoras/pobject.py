from abc import ABC, abstractmethod
from typing import TypedDict, Any, Self

class POProperties(TypedDict):
    name: str
    value: Any

class PObject(ABC):
    _args: list[str]
    _kwargs: list[tuple[str, Any]]
    _zord: int

    def __lt__(self, other: Self):
        return self._zord < other._zord

    @property
    @abstractmethod
    def tikz(self) -> str: pass

    @property
    @abstractmethod
    def pstricks(self) -> str: pass

    @property
    @abstractmethod
    def svg(self) -> str: pass