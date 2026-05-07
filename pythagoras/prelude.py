"""
This module brings all the names of the package into the global namespace.
This way, it is easier to import specific objects by writing

.. code-block:: python

   from pythagoras.prelude import Fill, BLACK, ...
"""

from .angle import *
from .arrow import *
from .canvas import *
from .circle import *
from .curve import *
from .label import *
from .line import *
from .pobject import *
from .r3.camera import *
from .r3.canvas import *
from .r3.curve import *
from .r3.mesh import *
from .r3.pobject import *
from .r3.rendering import *
from .r3.sphere import *
from .r3.vector import *
from .shape import *
from .style.color import *
from .style.draw import *
from .style.line import *
from .style.opacity import *
from .utils import *
from .vector import *
