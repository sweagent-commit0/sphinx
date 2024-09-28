"""Allow `MathJax`_ to be used to display math in Sphinx's HTML writer.

This requires the MathJax JavaScript library on your webserver/computer.

.. _MathJax: https://www.mathjax.org/
"""
from __future__ import annotations
import json
from typing import TYPE_CHECKING, Any, cast
from docutils import nodes
import sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.domains.math import MathDomain
from sphinx.errors import ExtensionError
from sphinx.locale import _
from sphinx.util.math import get_node_equation_number
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
    from sphinx.writers.html5 import HTML5Translator
MATHJAX_URL = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
logger = sphinx.util.logging.getLogger(__name__)