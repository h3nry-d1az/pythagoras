from pythagoras.prelude import Camera3D, Canvas, Cube, Point, project_point

ctx = Canvas(50)

for p in Cube((0, 0, 5), 5).vertices:
    if pp := project_point(Camera3D((-1, 0, 0)), 1, p):
        ctx.add(Point(*pp, 0.01))

print(ctx.svg())
