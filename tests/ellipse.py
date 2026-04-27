from pythagoras.prelude import Canvas, Ellipse, Point

ctx = Canvas()
ctx.scale = 100

ell = Ellipse.from_foci((1, 2), (3, -1), (2, 2))
p = Point(2, 2, 0.1)

ctx.add(ell)
ctx.add(p)
ctx.add(Point(1, 2, 0.1))
ctx.add(Point(3, -1, 0.1))

print(ctx.svg())
