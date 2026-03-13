from math import sqrt

from pythagoras import Canvas, Circle, Point

ctx = Canvas(0, 0)

cr = Circle(0, 0, 1, -1)

p1 = Point(0, 1, 0.05)
p2 = Point(1 / 2, sqrt(3) / 2, 0.05)
p3 = Point(sqrt(2) / 2, sqrt(2) / 2, 0.05)
p4 = Point(sqrt(3) / 2, 1 / 2, 0.05)
p5 = Point(1, 0, 0.05)

ctx.add(p1, p2, p3, p4, p5, cr)
print(ctx.svg())
