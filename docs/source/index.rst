Pythagoras
==========

Pythagoras is a Python package for creating geometrical constructions and
drawings, which can then be exported into SVG and TikZ code.

It was built in order to write the diagrams within the problems I post in
`my blog <https://h3nry-d1az.github.io/blog/>`_, without having to write
any SVG directly, and in such a way that transitioning into :math:`{\rm \LaTeX}` is
fairly straightforward.

Installation
------------

Since there are no pre-built wheels so far, you can choose to install the
latest stable release by cloning the repository, doing a ``git checkout`` to
its corresponding tag, and then executing::

   python3 -m pip install .

You may also fetch and install the package directly over the network by running::

   python3 -m pip install git+[canonical-url]

where ``[canonical-url]`` right now stands for https://github.com/h3nry-d1az/pythagoras.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
