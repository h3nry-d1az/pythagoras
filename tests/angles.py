from pythagoras import *

ctx = Canvas()
ctx.scale = 20

triangle = Polygon.triangle_from_lengths(13, 14, 15)
ctx.add(triangle)

ctx.add(Angle(triangle.points[1], triangle.points[0], triangle.points[2], 2.5))
ctx.add(Angle(triangle.points[0], triangle.points[1], triangle.points[2], 2.5))
ctx.add(Angle(triangle.points[0], triangle.points[2], triangle.points[1], 2.5))

print(ctx.svg())
