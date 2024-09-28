"""Docutils transforms used by Sphinx when reading documents."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, cast
from docutils import nodes
from sphinx import addnodes
from sphinx.transforms import SphinxTransform
if TYPE_CHECKING:
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

class RefOnlyListChecker(nodes.GenericNodeVisitor):
    """Raise `nodes.NodeFound` if non-simple list item is encountered.

    Here 'simple' means a list item containing only a paragraph with a
    single reference in it.
    """

    def invisible_visit(self, node: Node) -> None:
        """Invisible nodes should be ignored."""
        pass

class RefOnlyBulletListTransform(SphinxTransform):
    """Change refonly bullet lists to use compact_paragraphs.

    Specifically implemented for 'Indices and Tables' section, which looks
    odd when html_compact_lists is false.
    """
    default_priority = 100