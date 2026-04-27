from math import cos, pi, sin

from pythagoras.prelude import Canvas, Parametric

ctx = Canvas()
ctx.scale = 50

ctx.add(Parametric(lambda t: (t * cos(t * pi), t * sin(t * pi)), 0, 10, 0.001))

print(ctx.svg())
