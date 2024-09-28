"""The index domain."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, ClassVar
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.domains import Domain
from sphinx.util import logging
from sphinx.util.docutils import ReferenceRole, SphinxDirective
from sphinx.util.index_entries import split_index_msg
from sphinx.util.nodes import process_index_entry
if TYPE_CHECKING:
    from collections.abc import Iterable
    from docutils.nodes import Node, system_message
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
logger = logging.getLogger(__name__)

class IndexDomain(Domain):
    """Index domain."""
    name = 'index'
    label = 'index'

    def process_doc(self, env: BuildEnvironment, docname: str, document: Node) -> None:
        """Process a document after it is read by the environment."""
        pass

class IndexDirective(SphinxDirective):
    """
    Directive to add entries to the index.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[OptionSpec] = {'name': directives.unchanged}

class IndexRole(ReferenceRole):
    pass