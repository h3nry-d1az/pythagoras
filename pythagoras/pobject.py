from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self

__all__ = ["POProperty", "PObject", "RenderingContext"]


@dataclass
class RenderingContext:
    """
    Container class for the properties of a :class:`Canvas <pythagoras.canvas.Canvas>` object.
    Its main purpose is to be passed as an argument when calling :meth:`PObject.svg`
    or :meth:`PObject.tikz`.

    Attributes:
        scale: The scaling factor by which the canvas is stretched. When exporting to TikZ,
            this is compiled exactly into `[scale={scale}]`, and when using SVG, every
            distance is muliplied by its value.
        xmin: Minimum :math:`x`-coordinate across all the entities (without scaling).
        xmax: Maximum :math:`x`-coordinate across all the entities (without scaling).
        ymin: Minimum :math:`y`-coordinate across all the entities (without scaling).
        xmax: Maximum :math:`y`-coordinate across all the entities (without scaling).
    """

    scale: float
    xmin: float
    xmax: float
    ymin: float
    ymax: float

    @classmethod
    def from_dimensions(
        cls,
        scale: float,
        width: float,
        height: float,
        origin: tuple[float, float] = (0, 0),
    ) -> Self:
        """
        Construct a rendering context from its dimensions and its position in space.

        Returns:
            An instance of :class:`RenderingContext`.
        """
        return cls(
            scale,
            origin[0] - width / 2,
            origin[0] + width / 2,
            origin[1] - height / 2,
            origin[1] + height / 2,
        )

    @property
    def width(self) -> float:
        """
        Width of the canvas (after scaling).
        """
        return self.scale * (self.xmax - self.xmin) + 5

    @property
    def height(self) -> float:
        """
        Height of the canvas (after scaling).
        """
        return self.scale * (self.ymax - self.ymin) + 5

    @property
    def origin(self) -> tuple[float, float]:
        """
        Center of the canvas in the Cartesian plane (before scaling).
        """
        return ((self.xmax + self.xmin) / 2, (self.ymax + self.ymin) / 2)


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
    def tikz(self, ctx: RenderingContext, *args: POProperty) -> str:
        """
        Compiles the object into a sequence of TikZ instructions.

        Parameters:
            ctx: Context associated with the :class:`Canvas <pythagoras.canvas.Canvas>` instance.
            args: Properties of the object.

        Returns:
            The resulting TikZ code.
        """
        pass

    @abstractmethod
    def svg(self, ctx: RenderingContext, *args: POProperty) -> str:
        """
        Compiles the object into SVG commands.

        Parameters:
            ctx: Context associated with the :class:`Canvas <pythagoras.canvas.Canvas>` instance.
            args: Properties of the object.

        Returns:
            The corresponding SVG code.
        """
        pass
