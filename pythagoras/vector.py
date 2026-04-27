from dataclasses import dataclass
from math import hypot
from typing import Self

__all__ = ["Vector"]


@dataclass
class Vector:
    x: float
    y: float

    def __call__(self) -> tuple[float, float]:
        return (self.x, self.y)

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Self) -> Self:
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Self) -> Self:
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, alpha: float) -> Self:
        return self.__class__(self.x * alpha, self.y * alpha)

    def __rmul__(self, alpha: float) -> Self:
        return self * alpha

    def __matmul__(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y

    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y)

    def __abs__(self) -> float:
        return hypot(self.x, self.y)

    def __complex__(self) -> complex:
        return complex(self.x, self.y)
