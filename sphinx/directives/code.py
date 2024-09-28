from __future__ import annotations
import sys
import textwrap
from difflib import unified_diff
from typing import TYPE_CHECKING, Any, ClassVar
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.directives import optional_int
from sphinx.locale import __
from sphinx.util import logging, parselinenos
from sphinx.util.docutils import SphinxDirective
if TYPE_CHECKING:
    from docutils.nodes import Element, Node
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
logger = logging.getLogger(__name__)

class Highlight(SphinxDirective):
    """
    Directive to set the highlighting language for code blocks, as well
    as the threshold for line numbers.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec: ClassVar[OptionSpec] = {'force': directives.flag, 'linenothreshold': directives.positive_int}

class CodeBlock(SphinxDirective):
    """
    Directive for a code block with special highlighting or line numbering
    settings.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec: ClassVar[OptionSpec] = {'force': directives.flag, 'linenos': directives.flag, 'dedent': optional_int, 'lineno-start': int, 'emphasize-lines': directives.unchanged_required, 'caption': directives.unchanged_required, 'class': directives.class_option, 'name': directives.unchanged}

class LiteralIncludeReader:
    INVALID_OPTIONS_PAIR = [('lineno-match', 'lineno-start'), ('lineno-match', 'append'), ('lineno-match', 'prepend'), ('start-after', 'start-at'), ('end-before', 'end-at'), ('diff', 'pyobject'), ('diff', 'lineno-start'), ('diff', 'lineno-match'), ('diff', 'lines'), ('diff', 'start-after'), ('diff', 'end-before'), ('diff', 'start-at'), ('diff', 'end-at')]

    def __init__(self, filename: str, options: dict[str, Any], config: Config) -> None:
        self.filename = filename
        self.options = options
        self.encoding = options.get('encoding', config.source_encoding)
        self.lineno_start = self.options.get('lineno-start', 1)
        self.parse_options()

class LiteralInclude(SphinxDirective):
    """
    Like ``.. include:: :literal:``, but only warns if the include file is
    not found, and does not raise errors.  Also has several options for
    selecting what to include.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[OptionSpec] = {'dedent': optional_int, 'linenos': directives.flag, 'lineno-start': int, 'lineno-match': directives.flag, 'tab-width': int, 'language': directives.unchanged_required, 'force': directives.flag, 'encoding': directives.encoding, 'pyobject': directives.unchanged_required, 'lines': directives.unchanged_required, 'start-after': directives.unchanged_required, 'end-before': directives.unchanged_required, 'start-at': directives.unchanged_required, 'end-at': directives.unchanged_required, 'prepend': directives.unchanged_required, 'append': directives.unchanged_required, 'emphasize-lines': directives.unchanged_required, 'caption': directives.unchanged, 'class': directives.class_option, 'name': directives.unchanged, 'diff': directives.unchanged_required}