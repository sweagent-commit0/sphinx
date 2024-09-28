"""The JavaScript domain."""
from __future__ import annotations
import contextlib
from typing import TYPE_CHECKING, Any, ClassVar, cast
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.domains.python._annotations import _pseudo_parse_arglist
from sphinx.locale import _, __
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.docfields import Field, GroupedField, TypedField
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import make_id, make_refnode
if TYPE_CHECKING:
    from collections.abc import Iterator
    from docutils.nodes import Element, Node
    from sphinx.addnodes import desc_signature, pending_xref
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
logger = logging.getLogger(__name__)

class JSObject(ObjectDescription[tuple[str, str]]):
    """
    Description of a JavaScript object.
    """
    has_arguments = False
    allow_nesting = False
    option_spec: ClassVar[OptionSpec] = {'no-index': directives.flag, 'no-index-entry': directives.flag, 'no-contents-entry': directives.flag, 'no-typesetting': directives.flag, 'noindex': directives.flag, 'noindexentry': directives.flag, 'nocontentsentry': directives.flag, 'single-line-parameter-list': directives.flag}

    def handle_signature(self, sig: str, signode: desc_signature) -> tuple[str, str]:
        """Breaks down construct signatures

        Parses out prefix and argument list from construct definition. The
        namespace and class will be determined by the nesting of domain
        directives.
        """
        pass

    def before_content(self) -> None:
        """Handle object nesting before content

        :py:class:`JSObject` represents JavaScript language constructs. For
        constructs that are nestable, this method will build up a stack of the
        nesting hierarchy so that it can be later de-nested correctly, in
        :py:meth:`after_content`.

        For constructs that aren't nestable, the stack is bypassed, and instead
        only the most recent object is tracked. This object prefix name will be
        removed with :py:meth:`after_content`.

        The following keys are used in ``self.env.ref_context``:

            js:objects
                Stores the object prefix history. With each nested element, we
                add the object prefix to this list. When we exit that object's
                nesting level, :py:meth:`after_content` is triggered and the
                prefix is removed from the end of the list.

            js:object
                Current object prefix. This should generally reflect the last
                element in the prefix history
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

class JSCallable(JSObject):
    """Description of a JavaScript function, method or constructor."""
    has_arguments = True
    doc_field_types = [TypedField('arguments', label=_('Arguments'), names=('argument', 'arg', 'parameter', 'param'), typerolename='func', typenames=('paramtype', 'type')), GroupedField('errors', label=_('Throws'), rolename='func', names=('throws',), can_collapse=True), Field('returnvalue', label=_('Returns'), has_arg=False, names=('returns', 'return')), Field('returntype', label=_('Return type'), has_arg=False, names=('rtype',))]

class JSConstructor(JSCallable):
    """Like a callable but with a different prefix."""
    allow_nesting = True

class JSModule(SphinxDirective):
    """
    Directive to mark description of a new JavaScript module.

    This directive specifies the module name that will be used by objects that
    follow this directive.

    Options
    -------

    no-index
        If the ``:no-index:`` option is specified, no linkable elements will be
        created, and the module won't be added to the global module index. This
        is useful for splitting up the module definition across multiple
        sections or files.

    :param mod_name: Module name
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec: ClassVar[OptionSpec] = {'no-index': directives.flag, 'no-contents-entry': directives.flag, 'no-typesetting': directives.flag, 'noindex': directives.flag, 'nocontentsentry': directives.flag}

class JSXRefRole(XRefRole):
    pass

class JavaScriptDomain(Domain):
    """JavaScript language domain."""
    name = 'js'
    label = 'JavaScript'
    object_types = {'function': ObjType(_('function'), 'func'), 'method': ObjType(_('method'), 'meth'), 'class': ObjType(_('class'), 'class'), 'data': ObjType(_('data'), 'data'), 'attribute': ObjType(_('attribute'), 'attr'), 'module': ObjType(_('module'), 'mod')}
    directives = {'function': JSCallable, 'method': JSCallable, 'class': JSConstructor, 'data': JSObject, 'attribute': JSObject, 'module': JSModule}
    roles = {'func': JSXRefRole(fix_parens=True), 'meth': JSXRefRole(fix_parens=True), 'class': JSXRefRole(fix_parens=True), 'data': JSXRefRole(), 'attr': JSXRefRole(), 'mod': JSXRefRole()}
    initial_data: dict[str, dict[str, tuple[str, str]]] = {'objects': {}, 'modules': {}}