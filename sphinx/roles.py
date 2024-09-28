"""Handlers for additional ReST roles."""
from __future__ import annotations
import re
from typing import TYPE_CHECKING, Any
import docutils.parsers.rst.directives
import docutils.parsers.rst.roles
import docutils.parsers.rst.states
from docutils import nodes, utils
from sphinx import addnodes
from sphinx.locale import _, __
from sphinx.util import ws_re
from sphinx.util.docutils import ReferenceRole, SphinxRole
if TYPE_CHECKING:
    from collections.abc import Sequence
    from docutils.nodes import Element, Node, TextElement, system_message
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata, RoleFunction
generic_docroles = {'command': addnodes.literal_strong, 'dfn': nodes.emphasis, 'kbd': nodes.literal, 'mailheader': addnodes.literal_emphasis, 'makevar': addnodes.literal_strong, 'mimetype': addnodes.literal_emphasis, 'newsgroup': addnodes.literal_emphasis, 'program': addnodes.literal_strong, 'regexp': nodes.literal}

class XRefRole(ReferenceRole):
    """
    A generic cross-referencing role.  To create a callable that can be used as
    a role function, create an instance of this class.

    The general features of this role are:

    * Automatic creation of a reference and a content node.
    * Optional separation of title and target with `title <target>`.
    * The implementation is a class rather than a function to make
      customization easier.

    Customization can be done in two ways:

    * Supplying constructor parameters:
      * `fix_parens` to normalize parentheses (strip from target, and add to
        title if configured)
      * `lowercase` to lowercase the target
      * `nodeclass` and `innernodeclass` select the node classes for
        the reference and the content node

    * Subclassing and overwriting `process_link()` and/or `result_nodes()`.
    """
    nodeclass: type[Element] = addnodes.pending_xref
    innernodeclass: type[TextElement] = nodes.literal

    def __init__(self, fix_parens: bool=False, lowercase: bool=False, nodeclass: type[Element] | None=None, innernodeclass: type[TextElement] | None=None, warn_dangling: bool=False) -> None:
        self.fix_parens = fix_parens
        self.lowercase = lowercase
        self.warn_dangling = warn_dangling
        if nodeclass is not None:
            self.nodeclass = nodeclass
        if innernodeclass is not None:
            self.innernodeclass = innernodeclass
        super().__init__()

    def process_link(self, env: BuildEnvironment, refnode: Element, has_explicit_title: bool, title: str, target: str) -> tuple[str, str]:
        """Called after parsing title and target text, and creating the
        reference node (given in *refnode*).  This method can alter the
        reference node and must return a new (or the same) ``(title, target)``
        tuple.
        """
        pass

    def result_nodes(self, document: nodes.document, env: BuildEnvironment, node: Element, is_ref: bool) -> tuple[list[Node], list[system_message]]:
        """Called before returning the finished nodes.  *node* is the reference
        node if one was created (*is_ref* is then true), else the content node.
        This method can add other nodes and must return a ``(nodes, messages)``
        tuple (the usual return value of a role function).
        """
        pass

class AnyXRefRole(XRefRole):
    pass

class PEP(ReferenceRole):
    pass

class RFC(ReferenceRole):
    pass

class GUILabel(SphinxRole):
    amp_re = re.compile('(?<!&)&(?![&\\s])')

class MenuSelection(GUILabel):
    BULLET_CHARACTER = '‣'

class EmphasizedLiteral(SphinxRole):
    parens_re = re.compile('(\\\\\\\\|\\\\{|\\\\}|{|})')

class Abbreviation(SphinxRole):
    abbr_re = re.compile('\\((.*)\\)$', re.DOTALL)

class Manpage(ReferenceRole):
    _manpage_re = re.compile('^(?P<path>(?P<page>.+)[(.](?P<section>[1-9]\\w*)?\\)?)$')
code_role.options = {'class': docutils.parsers.rst.directives.class_option, 'language': docutils.parsers.rst.directives.unchanged}
specific_docroles: dict[str, RoleFunction] = {'download': XRefRole(nodeclass=addnodes.download_reference), 'any': AnyXRefRole(warn_dangling=True), 'pep': PEP(), 'rfc': RFC(), 'guilabel': GUILabel(), 'menuselection': MenuSelection(), 'file': EmphasizedLiteral(), 'samp': EmphasizedLiteral(), 'abbr': Abbreviation(), 'manpage': Manpage()}