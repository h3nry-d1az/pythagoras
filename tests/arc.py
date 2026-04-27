from math import pi

from pythagoras.prelude import Arc, Canvas, Polygon

ctx = Canvas()
ctx.scale = 50

triangle = Polygon.regular(0, 0, 1, 3)
ctx.add(triangle, fill="blue")

p0, p1 = triangle.points[:2]
cv = Arc.from_two_points_and_angle(p0, p1, pi)
ctx.add(cv)

print(ctx.svg())
