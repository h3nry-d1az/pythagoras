from pythagoras.prelude import (
    GOLD,
    LIGHT_BLUE,
    LIGHT_RED,
    RED,
    YELLOW,
    Canvas,
    Fill,
    Line,
    Point,
    Stroke,
    Triangle,
)

ctx = Canvas()
ctx.scale = 50
ctx.add(
    delta := Triangle(A := (1.22, 1.4), B := (3.68, 4.46), C := (7.68, 0.3)),
    Fill(LIGHT_BLUE),
)

# The circumcenter is the intersection of the side bisectors
ctx.add(Line.segment_bisector(A, B), Stroke(LIGHT_RED))
ctx.add(Line.segment_bisector(B, C), Stroke(LIGHT_RED))
ctx.add(Line.segment_bisector(C, A), Stroke(LIGHT_RED))

ctx.add(delta.circumcircle(), Stroke(RED))
ctx.add(Point(*delta.circumcenter, 0.1, zord=1), Fill(RED))

# The incenter is the intersection of the angle bisectors
ctx.add(Line.angle_bisector(B, A, C), Stroke(YELLOW))
ctx.add(Line.angle_bisector(A, B, C), Stroke(YELLOW))
ctx.add(Line.angle_bisector(A, C, B), Stroke(YELLOW))

ctx.add(delta.incircle()[0], Stroke(GOLD))
ctx.add(Point(*delta.incenter, 0.1, zord=1), Fill(GOLD))

print(ctx.svg())
