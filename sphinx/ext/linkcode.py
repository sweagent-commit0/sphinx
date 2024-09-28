"""Add external links to module code in Python object descriptions."""
from __future__ import annotations
from typing import TYPE_CHECKING
from docutils import nodes
import sphinx
from sphinx import addnodes
from sphinx.errors import SphinxError
from sphinx.locale import _
if TYPE_CHECKING:
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

class LinkcodeError(SphinxError):
    category = 'linkcode error'