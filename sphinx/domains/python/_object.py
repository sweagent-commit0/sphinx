from __future__ import annotations
import contextlib
import re
from typing import TYPE_CHECKING, ClassVar
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.addnodes import desc_signature, pending_xref, pending_xref_condition
from sphinx.directives import ObjectDescription
from sphinx.domains.python._annotations import _parse_annotation, _parse_arglist, _parse_type_list, _pseudo_parse_arglist, parse_reftarget
from sphinx.locale import _
from sphinx.util import logging
from sphinx.util.docfields import Field, GroupedField, TypedField
from sphinx.util.nodes import make_id
if TYPE_CHECKING:
    from docutils.nodes import Node
    from docutils.parsers.rst.states import Inliner
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import OptionSpec, TextlikeNode
logger = logging.getLogger(__name__)
py_sig_re = re.compile('^ ([\\w.]*\\.)?            # class name(s)\n          (\\w+)  \\s*             # thing name\n          (?: \\[\\s*(.*)\\s*])?    # optional: type parameters list\n          (?: \\(\\s*(.*)\\s*\\)     # optional: arguments\n           (?:\\s* -> \\s* (.*))?  #           return annotation\n          )? $                   # and nothing more\n          ', re.VERBOSE)

class PyXrefMixin:
    _delimiters_re = re.compile('(\\s*[\\[\\]\\(\\),](?:\\s*o[rf]\\s)?\\s*|\\s+o[rf]\\s+|\\s*\\|\\s*|\\.\\.\\.)')

class PyField(PyXrefMixin, Field):
    pass

class PyGroupedField(PyXrefMixin, GroupedField):
    pass

class PyTypedField(PyXrefMixin, TypedField):
    pass

class PyObject(ObjectDescription[tuple[str, str]]):
    """
    Description of a general Python object.

    :cvar allow_nesting: Class is an object that allows for nested namespaces
    :vartype allow_nesting: bool
    """
    option_spec: ClassVar[OptionSpec] = {'no-index': directives.flag, 'no-index-entry': directives.flag, 'no-contents-entry': directives.flag, 'no-typesetting': directives.flag, 'noindex': directives.flag, 'noindexentry': directives.flag, 'nocontentsentry': directives.flag, 'single-line-parameter-list': directives.flag, 'single-line-type-parameter-list': directives.flag, 'module': directives.unchanged, 'canonical': directives.unchanged, 'annotation': directives.unchanged}
    doc_field_types = [PyTypedField('parameter', label=_('Parameters'), names=('param', 'parameter', 'arg', 'argument', 'keyword', 'kwarg', 'kwparam'), typerolename='class', typenames=('paramtype', 'type'), can_collapse=True), PyTypedField('variable', label=_('Variables'), names=('var', 'ivar', 'cvar'), typerolename='class', typenames=('vartype',), can_collapse=True), PyGroupedField('exceptions', label=_('Raises'), rolename='exc', names=('raises', 'raise', 'exception', 'except'), can_collapse=True), Field('returnvalue', label=_('Returns'), has_arg=False, names=('returns', 'return')), PyField('returntype', label=_('Return type'), has_arg=False, names=('rtype',), bodyrolename='class')]
    allow_nesting = False

    def get_signature_prefix(self, sig: str) -> list[nodes.Node]:
        """May return a prefix to put before the object name in the
        signature.
        """
        pass

    def needs_arglist(self) -> bool:
        """May return true if an empty argument list is to be generated even if
        the document contains none.
        """
        pass

    def handle_signature(self, sig: str, signode: desc_signature) -> tuple[str, str]:
        """Transform a Python signature into RST nodes.

        Return (fully qualified name of the thing, classname if any).

        If inside a class, the current class name is handled intelligently:
        * it is stripped from the displayed name if present
        * it is added to the full name (return value) if not present
        """
        pass

    def get_index_text(self, modname: str, name: tuple[str, str]) -> str:
        """Return the text for the index entry of the object."""
        pass

    def before_content(self) -> None:
        """Handle object nesting before content

        :py:class:`PyObject` represents Python language constructs. For
        constructs that are nestable, such as a Python classes, this method will
        build up a stack of the nesting hierarchy so that it can be later
        de-nested correctly, in :py:meth:`after_content`.

        For constructs that aren't nestable, the stack is bypassed, and instead
        only the most recent object is tracked. This object prefix name will be
        removed with :py:meth:`after_content`.
        """
        pass

    def after_content(self) -> None:
        """Handle object de-nesting after content

        If this class is a nestable object, removing the last nested class prefix
        ends further nesting in the object.

        If this class is not a nestable object, the list of classes should not
        be altered as we didn't affect the nesting levels in
        :py:meth:`before_content`.
        """
        pass