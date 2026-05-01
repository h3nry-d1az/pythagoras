import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "Pythagoras"
copyright = "2026, Henry Díaz Bordón"
author = "Henry Díaz Bordón"
release = "0.1.0"


extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

autosummary_generate = True
napoleon_use_ivar = True

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "traditional"
html_static_path = ["_static"]
