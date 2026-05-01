from pythagoras.prelude import Canvas, Polygon, grid
from pythagoras.style import color
from pythagoras.style.draw import Fill
from pythagoras.style.line import Dashed
from pythagoras.style.opacity import FillOpacity

ctx = Canvas(50)

ctx.add(
    Polygon((-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), zord=1),
    Fill(color.LIGHT_BLUE),
    FillOpacity(0.5),
)
ctx.add_many(grid((-1, -1), (1, 1), (0.25, 0.5)), Dashed())

print(ctx.svg())
