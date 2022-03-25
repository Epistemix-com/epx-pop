# Configuration file template for Epistemix Documentation
#
# Please visit the doc-shared repository in GitHub for more information

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys

sys.path.insert(0, os.path.abspath("doc-shared/code"))
sys.path.insert(0, os.path.abspath("../epxpop"))
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))

# -- Shared settings -----------------------------------------------------

# These environment variable establish base names that are used in sharedconf.py
#   BASE_DIR holds base directory for this project
#   EPI_PROJECT holds the base name for this project
#   EPI_TITLE holds the document title for this project
#   EPI_SHORT_TITLE holds the short title for use in URLs or other references
os.environ["BASE_DIR"] = os.getcwd()
os.environ["EPI_PROJECT"] = str("epx-pop")
os.environ["EPI_TITLE"] = str("Epistemix Populations")
os.environ["EPI_SHORT_TITLE"] = str("Epistemix Populations")

from sharedconf import *

html_theme_options = {}

# -- Custom settings -----------------------------------------------------
# You can override the shared defaults here, if necessary

extensions.remove("sphinx.ext.napoleon")
extensions = extensions + [
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.imgmath",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]
html_theme = "pydata_sphinx_theme"
autodoc_member_order = "bysource"

autodoc_default_options = {
    "ignore-module-all": True,
}
