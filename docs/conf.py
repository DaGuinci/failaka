# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sphinx_rtd_theme  # noqa

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Failalka'
copyright = '2025, gevendev.net'
author = 'Guillaume Even'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinxcontrib.plantuml',
    'sphinx_rtd_dark_mode'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

master_doc = 'index'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_dark_mode'
html_static_path = ['_static']
html_css_files = [
    'css/erd.css',
]

html_show_sourcelink = False
# user starts in dark mode
default_dark_mode = True

# user starts in light mode
# default_dark_mode = False