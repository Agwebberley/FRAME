# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import django

# Add the project root to the path
sys.path.insert(0, os.path.abspath("../../"))
sys.path.insert(0, os.path.abspath("../../frame"))

os.environ["DJANGO_SETTINGS_MODULE"] = "docs.settings"
django.setup()

project = "FRAME"
copyright = "2024, Agwebberley"
author = "Agwebberley"
release = "0.9.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "myst_parser",
    "autodoc2",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

myst_enable_extensions = [
    "deflist",
    "fieldlist",
]

# -- Options for autodoc -----------------------------------------------------

autodoc2_packages = ["frame"]
autodoc2_render_plugin = "myst"
