from math import cos, pi, sin

from pythagoras.prelude import (
    GRAY,
    LIGHT_GRAY,
    Camera3D,
    Canvas,
    Canvas3D,
    LineWidth,
    Stroke,
    Trajectory,
)

ctx = Canvas(20)
scene = Canvas3D((50, 50), camera=Camera3D((3, 7.5, -10), (-0.3, -0.5, 1)), frustum=40)

scene.add(
    Trajectory(lambda t: (0, t, 0), 0, 2 * pi), Stroke(LIGHT_GRAY), LineWidth(0.05)
)
scene.add(
    Trajectory(lambda t: (0, 2 * pi, t), 0, 2 * pi), Stroke(GRAY), LineWidth(0.05)
)
scene.add(Trajectory(lambda t: (t * sin(t), t, t * cos(t)), 0, 2 * pi), LineWidth(0.05))

ctx.add(scene)
print(ctx.svg())
