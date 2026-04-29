from pythagoras.prelude import Canvas, Circle, Label, Path, Point, Polygon
from pythagoras.style import color
from pythagoras.style.draw import Fill, FontSize

ctx = Canvas()
ctx.scale = 20

triangle = Polygon.triangle_from_lengths(13, 14, 15)
circle, t1, t2, t3 = Circle.triangle_incircle(
    triangle.points[0], triangle.points[1], triangle.points[2], zord=-1
)

I = (circle.x, circle.y)

ctx.add(triangle)
ctx.add(circle, Fill(color.GRAY))
ctx.add(Path(triangle.points[0], I))
ctx.add(Path(triangle.points[1], I))
ctx.add(Path(triangle.points[2], I))
ctx.add(Label(I[0] + 1, I[1] + 1, "I"), FontSize(12))

ctx.add(Point(*t1, 0.25))
ctx.add(Point(*t2, 0.25))
ctx.add(Point(*t3, 0.25))

ctx.add(Polygon(triangle.points[0], I, triangle.points[1], zord=-2), Fill(color.GREEN))

print(ctx.svg())
