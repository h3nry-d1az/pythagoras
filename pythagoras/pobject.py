from abc import ABC, abstractmethod
from typing import Self

__all__ = ["POProperty", "PObject"]


class POProperty(ABC):
    """
    Abstract base class for a property of a :class:`PObject`.
    """

    @abstractmethod
    def tikz(self) -> str:
        """
        Compiles the property into TikZ syntax.

        Returns:
            The corresponding TikZ property.
        """
        pass

    @abstractmethod
    def svg(self) -> str:
        """
        Compiles the property into SVG syntax.

        Returns:
            The corresponding SVG property.
        """
        pass


class PObject(ABC):
    """
    Abstract base class for renderable objects.
    """

    _zord: int

    def __lt__(self, other: Self) -> bool:
        return self._zord < other._zord

    @abstractmethod
    def extrema(self) -> list[tuple[float, float]]:
        """
        Computes the furthermost points of the figure.

        Returns:
            A list with the bounding points of the object.
        """
        pass

    @abstractmethod
    def tikz(self, *args: POProperty) -> str:
        """
        Compiles the object into a sequence of TikZ instructions.

        Returns:
            The resulting TikZ code.
        """
        pass

    @abstractmethod
    def svg(
        self,
        origin: tuple[float, float],
        width: float,
        height: float,
        scale: float,
        *args: POProperty,
    ) -> str:
        """
        Compiles the object into SVG commands.

        Returns:
            The corresponding SVG code.
        """
        pass
