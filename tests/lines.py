from typing import cast

from pythagoras.prelude import (
    BLUE,
    GREEN,
    PURPLE,
    RED,
    YELLOW,
    Canvas,
    Circle,
    Dashed,
    Line,
    LineWidth,
    Phantom,
    Point,
    Stroke,
    Vector,
    grid,
)

ctx = Canvas(20)
ctx.add(Phantom(10, 12))
ctx.add(Phantom(-5, 1))
ctx.add_many(grid((-8, -10), (10, 12), (1, 1)), Dashed())

ctx.add(l1 := Line.from_implicit(-1, 2, 2), Stroke(RED))
assert (0, 1) in l1
assert (1, 1) not in l1

ctx.add(l2 := Line.from_implicit(5, 1, 9), Stroke(BLUE))
ctx.add(l3 := Line((-3, 3), Vector(1, 1 / 8)), Stroke(GREEN))
ctx.add(l4 := Line.from_two_points((-4.5, 0), (-4.5, 2)), Stroke(YELLOW), LineWidth(3))

ctx.add(Point(*cast(tuple[float, float], l1 & l2), 0.25))
ctx.add(Point(*cast(tuple[float, float], l1 & l3), 0.25))
ctx.add(Point(*cast(tuple[float, float], l2 & l3), 0.25))
assert Line.from_two_points((-3, 0), (-3, 1)) & l4 is None

ctx.add(c := Circle(3, 4, 5), Stroke(PURPLE), LineWidth(2))
p1, p2 = l1 & c
ctx.add(Point(*cast(tuple[float, float], p1), 0.25))
ctx.add(Point(*cast(tuple[float, float], p2), 0.25))

print(ctx.svg())
