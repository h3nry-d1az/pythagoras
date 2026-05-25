from typing import cast

from pythagoras.prelude import Canvas, Ellipse, Line, Point

ctx = Canvas()
ctx.scale = 100

ell = Ellipse.from_foci((1, 2), (3, -1), (2, 2))
p = Point(2, 2, 0.1)

ctx.add(ell)
ctx.add(p)
ctx.add(Point(1, 2, 0.1))
ctx.add(Point(3, -1, 0.1))

line = Line.from_two_points((2, 1), (0, 0))
ctx.add(line)

for p in line & ell:
    ctx.add(Point(*cast(tuple[float, float], p), 0.1))

print(ctx.svg())
