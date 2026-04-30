from dataclasses import dataclass
from math import cos, hypot, sin
from typing import Self

__all__ = ["Vector"]


@dataclass
class Vector:
    x: float
    y: float

    @classmethod
    def from_two_points(cls, p1: tuple[float, float], p2: tuple[float, float]) -> Self:
        return cls(p2[0] - p1[0], p2[1] - p1[1])

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

    def __imul__(self, alpha: float) -> Self:
        self.x *= alpha
        self.y *= alpha
        return self

    def __truediv__(self, alpha: float) -> Self:
        return self.__class__(self.x / alpha, self.y / alpha)

    def __itruediv__(self, alpha: float) -> Self:
        self.x /= alpha
        self.y /= alpha
        return self

    def __matmul__(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y

    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y)

    def __abs__(self) -> float:
        return hypot(self.x, self.y)

    def __complex__(self) -> complex:
        return complex(self.x, self.y)

    def __lshift__(self, angle: float) -> Self:
        return self.__class__(
            self.x * cos(angle) - self.y * sin(angle),
            self.x * sin(angle) + self.y * cos(angle),
        )

    def __rshift__(self, angle: float) -> Self:
        return self.__class__(
            self.x * cos(angle) + self.y * sin(angle),
            -self.x * sin(angle) + self.y * cos(angle),
        )

    def __ilshift__(self, angle: float) -> Self:
        x, y = self.x, self.y
        self.x = x * cos(angle) - y * sin(angle)
        self.y = x * sin(angle) + y * cos(angle)
        return self

    def __irshift__(self, angle: float) -> Self:
        x, y = self.x, self.y
        self.x = x * cos(angle) - y * sin(angle)
        self.y = -x * sin(angle) + y * cos(angle)
        return self

    @property
    def perp(self) -> Self:
        return self.__class__(-self.y, self.x)
