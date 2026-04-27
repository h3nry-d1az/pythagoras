from collections.abc import Iterable
from itertools import chain

from .pobject import POProperty

__all__ = [
    "compile_options_svg",
    "compile_options_tikz",
    "svg_command",
    "svg_path",
    "tikz_command",
]
__options_dict = {
    "fill": ("fill", "fill"),
    "color": ("color", "stroke"),
    "thickness": ("line width", "stroke-width"),
}


def tikz_command(name: str, body: str, *args: str, **kwargs: POProperty) -> str:
    if args or kwargs:
        kwargs_ = (f"{p[0]}={p[1]}" for p in sorted(kwargs.items(), key=lambda p: p[0]))
        params = f"{', '.join(chain(args, kwargs_))}"
    else:
        params = ""
    return rf"\{name}[{params}] {body};"


def svg_command(name: str, *args: str, **kwargs: POProperty) -> str:
    if args or kwargs:
        kwargs_ = (
            f'{p[0]}="{p[1] if isinstance(p[1], str) else round(p[1], 4)}"'
            for p in kwargs.items()
        )
        params = " ".join(chain(args, kwargs_))
    else:
        params = ""
    return rf"<{name} {params} />"


def compile_options_tikz(config: dict[str, POProperty]) -> None:
    for k, (v, _) in __options_dict.items():
        if k in config and k != v:
            config[v] = config[k]
            del config[k]


def compile_options_svg(config: dict[str, POProperty]) -> None:
    for k, (_, v) in __options_dict.items():
        if k in config and k != v:
            config[v] = config[k]
            del config[k]


def svg_path(
    points: Iterable[tuple[float, float]],
    origin: tuple[float, float],
    width: float,
    height: float,
    scale: float,
    *args: str,
    **kwargs: str | float,
) -> str:
    iterator = iter(points)
    p0 = next(iterator)
    path = f"M {p0[0] - origin[0]:.4f} {p0[1] + origin[1]:.4f}"
    for p in iterator:
        path += f" L {p[0] - origin[0]:.4f} {p[1] + origin[1]:.4f}"
    return svg_command("path", *args, d=path, **kwargs)
