from pythagoras import Canvas, Circle, Point
from math import sqrt

ctx = Canvas()

cr = Circle(0, 0, 1, -1)

p1 = Point(0, 1, .05)
p2 = Point(1/2, sqrt(3)/2, .05)
p3 = Point(sqrt(2)/2, sqrt(2)/2, .05)
p4 = Point(sqrt(3)/2, 1/2, .05)
p5 = Point(1, 0, .05)

ctx.add(p1, p2, p3, p4, p5, cr)
print(ctx.elements)
print(ctx.tikz_doc)