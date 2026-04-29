from collections.abc import Iterable

from .pobject import POProperty

__all__ = ["svg_command", "svg_path", "tikz_command"]


class __svg_d(POProperty):
    path: str

    def __init__(self, path: str) -> None:
        self.path = path

    def svg(self) -> str:
        return f'd="{self.path}"'

    def tikz(self) -> str:
        return super().tikz()


def tikz_command(name: str, body: str, *args: POProperty) -> str:
    params = f"[{', '.join(p.tikz() for p in args)}]" if args else ""
    return rf"\{name}{params} {body};"


def svg_command(name: str, *args: POProperty) -> str:
    params = " ".join(p.svg() for p in args) if args else ""
    return rf"<{name} {params} />"


def svg_path(
    points: Iterable[tuple[float, float]],
    origin: tuple[float, float],
    width: float,
    height: float,
    scale: float,
    *args: POProperty,
) -> str:
    iterator = iter(points)
    p0 = next(iterator)
    path = f"M {p0[0] - origin[0]:.4f} {p0[1] + origin[1]:.4f}"
    for p in iterator:
        path += f" L {p[0] - origin[0]:.4f} {p[1] + origin[1]:.4f}"
    return svg_command("path", __svg_d(path), *args)
