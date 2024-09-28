"""transforms for code-blocks."""
from __future__ import annotations
import sys
from typing import TYPE_CHECKING, Any, NamedTuple
from docutils import nodes
from pygments.lexers import PythonConsoleLexer, guess_lexer
from sphinx import addnodes
from sphinx.ext import doctest
from sphinx.transforms import SphinxTransform
if TYPE_CHECKING:
    from docutils.nodes import Node, TextElement
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

class HighlightSetting(NamedTuple):
    language: str
    force: bool
    lineno_threshold: int

class HighlightLanguageTransform(SphinxTransform):
    """
    Apply highlight_language to all literal_block nodes.

    This refers both :confval:`highlight_language` setting and
    :rst:dir:`highlight` directive.  After processing, this transform
    removes ``highlightlang`` node from doctree.
    """
    default_priority = 400

class HighlightLanguageVisitor(nodes.NodeVisitor):

    def __init__(self, document: nodes.document, default_language: str) -> None:
        self.default_setting = HighlightSetting(default_language, False, sys.maxsize)
        self.settings: list[HighlightSetting] = []
        super().__init__(document)

class TrimDoctestFlagsTransform(SphinxTransform):
    """
    Trim doctest flags like ``# doctest: +FLAG`` from python code-blocks.

    see :confval:`trim_doctest_flags` for more information.
    """
    default_priority = HighlightLanguageTransform.default_priority + 1