from itertools import chain
from math import cos, pi, sin
from typing import cast

from pythagoras.prelude import (
    Canvas,
    Circle,
    Ellipse,
    Line,
    Parametric,
    Point,
    Triangle,
)

ctx = Canvas(50)

circ = Circle(2, 2, 1.5)
ell = Ellipse.from_foci((1, 0), (0, 1), (1, 1))
line = Line.from_two_points((2, 0), (1, 0.5))
param = Parametric(lambda t: (t * cos(t) + 1, t * sin(t) + 2), 0, pi)
triangle = Triangle((-1, -1), (0, -1.5), (1, 4))
triangle2 = Triangle((0, 2), (2, 0), (2, 2))

ctx.add_many((circ, ell, line, param, triangle, triangle2))

for p in chain(
    triangle & ell,
    triangle & param,
    triangle & line,
    triangle & circ,
    triangle & triangle2,
    line & ell,
):
    p = cast(tuple[float, float], p)
    ctx.add(Point(*p, 0.05))

print(ctx.svg())
