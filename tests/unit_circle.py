from math import sqrt

from pythagoras import Canvas, Circle, Point

ctx = Canvas(125, 125)
ctx.scale = 50

ctx.add(p1 := Point(0, 1, 0.05), fill="red")
ctx.add(p2 := Point(1 / 2, sqrt(3) / 2, 0.05))
ctx.add(p3 := Point(sqrt(2) / 2, sqrt(2) / 2, 0.05))
ctx.add(Point(sqrt(3) / 2, 1 / 2, 0.05))
ctx.add(Point(1, 0, 0.05))
ctx.add(Circle.from_three_points((p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y), -1))

print(ctx.svg())
