from pythagoras.prelude import Canvas, Circle, Label, Path, Point, Polygon

ctx = Canvas()
ctx.scale = 20

triangle = Polygon.triangle_from_lengths(13, 14, 15)
circle, t1, t2, t3 = Circle.triangle_incenter(
    triangle.points[0], triangle.points[1], triangle.points[2], zord=-1
)

I = (circle.x, circle.y)

ctx.add(triangle)
ctx.add(circle, fill="gray")
ctx.add(Path(triangle.points[0], I))
ctx.add(Path(triangle.points[1], I))
ctx.add(Path(triangle.points[2], I))
ctx.add(Label(I[0] + 1, I[1] + 1, "I"), font_scale=2.5)

ctx.add(Point(*t1, 0.25))
ctx.add(Point(*t2, 0.25))
ctx.add(Point(*t3, 0.25))

ctx.add(Polygon(triangle.points[0], I, triangle.points[1], zord=-2), fill="green")

print(ctx.svg())
