from dataclasses import dataclass
from typing import Any

from ..pobject import POProperty as __POProperty
from . import color, draw


@dataclass
class CustomStyle(__POProperty):
    param: str
    value: Any

    def svg(self) -> str:
        return f'{self.param}="{self.value}"'

    def tikz(self) -> str:
        return f"{self.param}={self.value}"


__all__ = ["color", "draw"]
