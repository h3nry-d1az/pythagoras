from typing import cast

from pythagoras.prelude import (
    BLUE,
    GOLD,
    LIGHT_BLUE,
    LIGHT_RED,
    RED,
    Canvas,
    Fill,
    FillOpacity,
    Line,
    Point,
    Stroke,
    Triangle,
)

ctx = Canvas(50)

triangle = Triangle((0, 1), (3, 0), (1.5, 2))
euler = triangle.euler_line()
ctx.add(triangle, Fill(LIGHT_RED), FillOpacity(0.35))
ctx.add(euler)

ctx.add(Line.from_two_points(triangle.A, triangle.B))
ctx.add(Line.from_two_points(triangle.B, triangle.C))
ctx.add(Line.from_two_points(triangle.C, triangle.A))

for p in euler & triangle:
    p = cast(tuple[float, float], p)
    ctx.add(Point(*p, 0.05, zord=1), Fill(GOLD))

ctx.add(triangle.incircle()[0], Stroke(RED))
ctx.add(triangle.circumcircle(), Stroke(RED))
ctx.add((ea := triangle.excircle_A())[0], Stroke(BLUE))
ctx.add(Point(*ea[1], 0.05), Fill(LIGHT_BLUE))
ctx.add(Point(*ea[2], 0.05), Fill(LIGHT_BLUE))
ctx.add(Point(*ea[3], 0.05), Fill(LIGHT_BLUE))
ctx.add((eb := triangle.excircle_B())[0], Stroke(BLUE))
ctx.add(Point(*eb[1], 0.05), Fill(LIGHT_BLUE))
ctx.add(Point(*eb[2], 0.05), Fill(LIGHT_BLUE))
ctx.add(Point(*eb[3], 0.05), Fill(LIGHT_BLUE))
ctx.add((ec := triangle.excircle_C())[0], Stroke(BLUE))
ctx.add(Point(*ec[1], 0.05), Fill(LIGHT_BLUE))
ctx.add(Point(*ec[2], 0.05), Fill(LIGHT_BLUE))
ctx.add(Point(*ec[3], 0.05), Fill(LIGHT_BLUE))
ctx.add(triangle.nine_point_circle(), Stroke(RED))

ctx.add(Point(*triangle.orthocenter, 0.05, zord=1), Fill(LIGHT_RED))
ctx.add(Point(*triangle.centroid, 0.05, zord=1), Fill(LIGHT_RED))
ctx.add(Point(*triangle.incenter, 0.05, zord=1), Fill(LIGHT_RED))
ctx.add(Point(*triangle.circumcenter, 0.05, zord=1), Fill(LIGHT_RED))
ctx.add(Point(*triangle.npcenter, 0.05, zord=1), Fill(LIGHT_RED))

ctx.add(triangle.homothety(triangle.A, 2), Stroke(GOLD))

print(ctx.svg())
