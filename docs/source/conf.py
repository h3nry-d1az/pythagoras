import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "Pythagoras"
copyright = "2026, Henry Díaz Bordón"
author = "Henry Díaz Bordón"
release = "0.0.2"


extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.viewcode"]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "classic"
html_static_path = ["_static"]
