from collections.abc import Iterable

from .pobject import POProperty
from .style import CustomStyle

__all__ = ["svg_command", "svg_path", "tikz_command"]


def tikz_command(name: str, body: str, *args: POProperty) -> str:
    r"""
    Put together a TikZ command from its components.

    Parameters:
        name: Name of the command, that is, `\\{name}`.
        body: What goes between the command arguments and the final semicolon.
        *args: Arguments of the command -- i.e., `\\{name}[args]` -- as :class:`POProperty<pythagoras.pobject.POProperty>`'s.

    Returns:
        A valid TikZ command.
    """
    params = f"[{', '.join(p.tikz() for p in args)}]" if args else ""
    return rf"\{name}{params} {body};"


def svg_command(name: str, *args: POProperty) -> str:
    """
    Put together an SVG command from its components.

    Parameters:
        name: Name of the command, that is, `<{name}>`.
        *args: Parameters of the command, which correspond to key-value pairs
            when compiled, but are given as :class:`POProperty<pythagoras.pobject.POProperty>`'s.

    Returns:
        A valid SVG command.
    """
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
    """
    Construct an SVG path from its points.

    Parameters:
        points: The sequence of points (in the SVG coordinate system) that make up the path.
        origin: Origin of the frame of reference.
        width: Width of the figure.
        height: Height of the figure.
        scale: Scaling factor of the figure.
        *args: Additional properties of the path.

    Returns:
        Final `<path d="...">` tag.
    """
    iterator = iter(points)
    p0 = next(iterator)
    path = f"M {p0[0] - origin[0]:.4f} {p0[1] + origin[1]:.4f}"
    for p in iterator:
        path += f" L {p[0] - origin[0]:.4f} {p[1] + origin[1]:.4f}"
    return svg_command("path", CustomStyle("d", path), *args)


def fill_default_args(
    args: Iterable[POProperty], *defaults: tuple[type, POProperty]
) -> list[POProperty]:
    """
    Complete a list of :class:`POProperty<pythagoras.pobject.POProperty>`'s with default values for the types that are missing.

    Parameters:
        args: Initial set of properties.
        defaults: List of types with their default values.

    Returns:
        The completion of `args`.
    """
    xs = list(args)
    for q, e in defaults:
        if not any(isinstance(x, q) for x in args):
            xs.append(e)
    return xs
