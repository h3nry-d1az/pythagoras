from math import cos, pi, sin

from pythagoras.prelude import Canvas, ParametricCurve

ctx = Canvas()
ctx.scale = 100

ctx.add(ParametricCurve(lambda t: (t * cos(t * pi), t * sin(t * pi)), 0, 10, 0.001))

print(ctx.svg())
