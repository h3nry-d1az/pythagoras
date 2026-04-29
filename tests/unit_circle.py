from math import sqrt

from pythagoras.prelude import Canvas, Circle, Label, Point
from pythagoras.style import color
from pythagoras.style.draw import Fill, FontSize

ctx = Canvas()
ctx.scale = 50

ctx.add(p1 := Point(0, 1, 0.05), Fill(color.RED))
ctx.add(p2 := Point(1 / 2, sqrt(3) / 2, 0.05))
ctx.add(p3 := Point(sqrt(2) / 2, sqrt(2) / 2, 0.05))
ctx.add(Point(sqrt(3) / 2, 1 / 2, 0.05))
ctx.add(Point(1, 0, 0.05))
ctx.add(Circle.triangle_circumcircle((p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y), -1))
ctx.add(Label(0, 0, r"\omega"), FontSize(12))

print(ctx.svg())
