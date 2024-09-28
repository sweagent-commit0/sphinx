"""Single HTML builders."""
from __future__ import annotations
from os import path
from typing import TYPE_CHECKING, Any
from docutils import nodes
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment.adapters.toctree import global_toctree_for_doc
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.console import darkgreen
from sphinx.util.display import progress_message
from sphinx.util.nodes import inline_all_toctrees
if TYPE_CHECKING:
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class SingleFileHTMLBuilder(StandaloneHTMLBuilder):
    """
    A StandaloneHTMLBuilder subclass that puts the whole document tree on one
    HTML page.
    """
    name = 'singlehtml'
    epilog = __('The HTML page is in %(outdir)s.')
    copysource = False