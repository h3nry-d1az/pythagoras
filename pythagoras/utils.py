__all__ = ["cartesian_to_canvas"]


def cartesian_to_canvas(
    x: float, y: float, width: float, height: float, scale: float
) -> tuple[float, float]:
    return (width / 2 + x * scale, height / 2 - y * scale)
