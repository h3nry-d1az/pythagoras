from pythagoras.angle import Angle, RAngle
from pythagoras.canvas import Canvas
from pythagoras.shape import Polygon

ctx = Canvas()
ctx.scale = 50

# triangle = Polygon((0, 0), (4, 0), (4, 3))
triangle = Polygon.triangle_from_lengths(3, 4, 5)
triangle.rotate((0, 0), 20)
ctx.add(triangle)

ctx.add(Angle(triangle.points[1], triangle.points[0], triangle.points[2], 1))
ctx.add(Angle(triangle.points[2], triangle.points[1], triangle.points[0], 1))
ctx.add(RAngle(triangle.points[0], triangle.points[2], triangle.points[1], 0.75))

print(ctx.svg())
