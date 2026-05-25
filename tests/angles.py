from pythagoras.angle import Angle, RAngle
from pythagoras.canvas import Canvas
from pythagoras.triangle import Triangle

ctx = Canvas()
ctx.scale = 50

# triangle = Polygon((0, 0), (4, 0), (4, 3))
triangle = Triangle.from_lengths(3, 4, 5)
triangle.rotate((0, 0), 20)
ctx.add(triangle)

ctx.add(Angle(triangle.B, triangle.A, triangle.C, 1))
ctx.add(Angle(triangle.C, triangle.B, triangle.A, 1))
ctx.add(RAngle(triangle.A, triangle.C, triangle.B, 0.75))

print(ctx.svg())
