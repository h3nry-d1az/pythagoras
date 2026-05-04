from pythagoras.prelude import (
    BLUE,
    PURPLE,
    RED,
    Arrow,
    Canvas,
    Dashed,
    Fill,
    Opacity,
    Stroke,
    Vector,
)

ctx = Canvas(50)

v1 = Vector(4, 2)
v2 = Vector(1, 5)
s = v1 + v2

ctx.add(Arrow((0, 0), v1(), 0.5), Stroke(RED), Fill(RED))
ctx.add(Arrow((0, 0), v2(), 0.5), Stroke(BLUE), Fill(BLUE))
ctx.add(Arrow((0, 0), s(), 0.5, zord=1), Stroke(PURPLE), Fill(PURPLE))
ctx.add(Arrow(v1(), s(), 0.25), Stroke(BLUE), Fill(BLUE), Dashed(), Opacity(0.5))
ctx.add(Arrow(v2(), s(), 0.25), Stroke(RED), Fill(RED), Dashed(), Opacity(0.5))

print(ctx.svg())
