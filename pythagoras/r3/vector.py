from dataclasses import dataclass
from math import hypot
from typing import Self

__all__ = ["Vector3D"]


@dataclass
class Vector3D:
    """
    Three-dimensional vector with common operations.

    Attributes:
        x: :math:`x` component of the vector.
        y: :math:`y` component of the vector.
        z: :math:`z` component of the vector.
    """

    x: float
    y: float
    z: float

    @classmethod
    def from_two_points(
        cls, p1: tuple[float, float, float], p2: tuple[float, float, float]
    ) -> Self:
        """
        Constructor for the vector that joins two points.

        Parameters:
            p1: Initial point.
            p2: End point.

        Returns:
            The vector that goes from `p1` to `p2`.
        """
        return cls(p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])

    def __call__(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other: Self) -> Self:
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other: Self) -> Self:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, alpha: float) -> Self:
        return self.__class__(self.x * alpha, self.y * alpha, self.z * alpha)

    def __rmul__(self, alpha: float) -> Self:
        return self * alpha

    def __imul__(self, alpha: float) -> Self:
        self.x *= alpha
        self.y *= alpha
        self.z *= alpha
        return self

    def __truediv__(self, alpha: float) -> Self:
        return self.__class__(self.x / alpha, self.y / alpha, self.z / alpha)

    def __itruediv__(self, alpha: float) -> Self:
        self.x /= alpha
        self.y /= alpha
        self.z /= alpha
        return self

    def __matmul__(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __xor__(self, other: Self) -> Self:
        return self.__class__(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def __ixor__(self, other: Self) -> Self:
        x, y, z = self.x, self.y, self.z
        self.x = y * other.z - z * other.y
        self.y = z * other.x - x * other.z
        self.z = x * other.y - y * other.x
        return self

    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y, -self.z)

    def __abs__(self) -> float:
        return hypot(self.x, self.y, self.z)
