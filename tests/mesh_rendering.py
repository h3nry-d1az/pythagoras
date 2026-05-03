from pythagoras.prelude import (
    LIGHT_BLUE,
    Camera3D,
    Canvas,
    Canvas3D,
    Fill,
    FillOpacity,
    Mesh,
)

ctx = Canvas(10)

# If you run this to output TikZ, change the scale to .1 to avoid
# getting a `dimension too large` error
scene = Canvas3D((100, 100), (0, 0), Camera3D((0, 10, -500)), 1, 1000)

with open("tree.obj") as f:
    scene.add(Mesh.from_obj(f.read(), True, 0, Fill(LIGHT_BLUE), FillOpacity(0.5)))

ctx.add(scene)
print(ctx.svg())
