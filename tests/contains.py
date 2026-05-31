from math import cos, pi, sin

from pythagoras.prelude import Circle, Ellipse, Parametric, Polygon, Triangle

circ = Circle(1, 3, 4)
ell = Ellipse.from_foci((1, 2), (5, 6), (0.25, 3.2))
par = Parametric(f := lambda t: (t * cos(t), t * sin(t)), 0, 2 * pi, 0.1)
poly = Polygon((1, 1), (-1, 1), (-1, -1), (1, -1))
delta = Triangle((-1, 1), (1, 3), (2, -3))

assert (1 + 4 * cos(pi / 4), 3 + 4 * sin(pi / 4)) in circ
assert (0.25, 3.2) in ell
assert f(1) in par
assert (0, 1) in poly
assert (0, 1) in delta
