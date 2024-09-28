"""Allow todos to be inserted into your documentation.

Inclusion of todos can be switched of by a configuration variable.
The todolist directive collects all todos of your project and lists them along
with a backlink to the original location.
"""
from __future__ import annotations
import functools
import operator
from typing import TYPE_CHECKING, Any, ClassVar, cast
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
import sphinx
from sphinx import addnodes
from sphinx.domains import Domain
from sphinx.errors import NoUri
from sphinx.locale import _, __
from sphinx.util import logging, texescape
from sphinx.util.docutils import SphinxDirective, new_document
if TYPE_CHECKING:
    from docutils.nodes import Element, Node
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
    from sphinx.writers.html5 import HTML5Translator
    from sphinx.writers.latex import LaTeXTranslator
logger = logging.getLogger(__name__)

class todo_node(nodes.Admonition, nodes.Element):
    pass

class todolist(nodes.General, nodes.Element):
    pass

class Todo(BaseAdmonition, SphinxDirective):
    """
    A todo entry, displayed (if configured) in the form of an admonition.
    """
    node_class = todo_node
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec: ClassVar[OptionSpec] = {'class': directives.class_option, 'name': directives.unchanged}

class TodoDomain(Domain):
    name = 'todo'
    label = 'todo'

class TodoList(SphinxDirective):
    """
    A list of all todo entries.
    """
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec: ClassVar[OptionSpec] = {}

class TodoListProcessor:

    def __init__(self, app: Sphinx, doctree: nodes.document, docname: str) -> None:
        self.builder = app.builder
        self.config = app.config
        self.env = app.env
        self.domain = cast(TodoDomain, app.env.get_domain('todo'))
        self.document = new_document('')
        self.process(doctree, docname)

    def resolve_reference(self, todo: todo_node, docname: str) -> None:
        """Resolve references in the todo content."""
        pass