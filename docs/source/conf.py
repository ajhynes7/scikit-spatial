# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import sphinx_bootstrap_theme
from sphinx_gallery.sorting import ExplicitOrder

sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))

import skspatial  # noqa


# -- Project information -----------------------------------------------------

project = 'scikit-spatial'
copyright = '2019, Andrew Hynes'  # noqa
author = 'Andrew Hynes'

# The short X.Y version
version = skspatial.__version__


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'matplotlib.sphinxext.plot_directive',
    'numpydoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx_gallery.gen_gallery',
]

intersphinx_mapping = {
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    'matplotlib': ('http://matplotlib.org/', None),
}

sphinx_gallery_conf = {
    'examples_dirs': '../../examples',  # Path to example scripts
    'gallery_dirs': 'gallery',  # Path to save generated examples
    'download_all_examples': False,
    'subsection_order': ExplicitOrder(
        [
            '../../examples/projection',
            '../../examples/intersection',
            '../../examples/fitting',
            '../../examples/triangle',
        ],
    ),
}

autosummary_generate = True

# Prevent warnings about nonexisting documents
numpydoc_show_class_members = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'bootswatch_theme': 'cosmo',
    'globaltoc_depth': -1,
    'navbar_links': [
        ('Objects', 'objects/toc'),
        ('Plotting', 'plotting'),
        ('Gallery', 'gallery/index'),
        ('API', 'api_reference/toc'),
    ],
    'navbar_pagenav': False,
    'navbar_sidebarrel': False,
    'source_link_position': None,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'scikit-spatialdoc'


# -- Options for LaTeX output ------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'scikit-spatial.tex', 'scikit-spatial Documentation', 'Andrew Hynes', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, 'scikit-spatial', 'scikit-spatial Documentation', [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        'scikit-spatial',
        'scikit-spatial Documentation',
        author,
        'scikit-spatial',
        'One line description of project.',
        'Miscellaneous',
    ),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']
