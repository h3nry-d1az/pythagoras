from math import cos, pi, sin

from pythagoras.prelude import LIGHT_BLUE, Camera3D, Canvas, Canvas3D, Fill, Mesh

ctx = Canvas(20)
scene = Canvas3D(
    (50, 50), camera=Camera3D((0, 121.75, -100), (0, -1.2, 1)), frustum=1000
)

scene.add(
    Mesh.parametric(
        lambda u, v: (u * sin(v), v, u * cos(v)),
        (0, 2),
        (0, 2 * pi),
        (0.1, pi / 10),
        shaded=True,
    ),
    Fill(LIGHT_BLUE),
)

scene.add_light_source((0, 2 * pi + 1, 0), 2000)

ctx.add(scene)
print(ctx.svg())
