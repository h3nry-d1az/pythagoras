from abc import ABC, abstractmethod
from typing import Self

from ..pobject import POProperty
from .camera import Camera3D

__all__ = ["PObject3D"]


class PObject3D(ABC):
    """
    Abstract base class for a three-dimensional, renderable object. Behaves in an
    analogous fashion to a :class:`PObject <pythagoras.pobject.PObject>`.
    """

    _zord: int

    def __lt__(self, other: Self) -> bool:
        return self._zord < other._zord

    @abstractmethod
    def tikz(self, camera: Camera3D, frustum: float, *args: POProperty) -> str:
        """
        Compiles the 3D object into a sequence of TikZ instructions.

        Returns:
            The resulting TikZ code.
        """
        pass

    @abstractmethod
    def svg(
        self,
        camera: Camera3D,
        frustum: float,
        width: float,
        height: float,
        scale: float,
        *args: POProperty,
    ) -> str:
        """
        Compiles the 3D object into SVG commands.

        Returns:
            The corresponding SVG code.
        """
        pass
