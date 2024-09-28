"""Utility code for "Doc fields".

"Doc fields" are reST field lists in object descriptions that will
be domain-specifically transformed to a more appealing presentation.
"""
from __future__ import annotations
import contextlib
from typing import TYPE_CHECKING, Any, cast
from docutils import nodes
from docutils.nodes import Element, Node
from sphinx import addnodes
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.nodes import get_node_line
if TYPE_CHECKING:
    from docutils.parsers.rst.states import Inliner
    from sphinx.directives import ObjectDescription
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import TextlikeNode
logger = logging.getLogger(__name__)

def _is_single_paragraph(node: nodes.field_body) -> bool:
    """True if the node only contains one paragraph (and system messages)."""
    pass

class Field:
    """A doc field that is never grouped.  It can have an argument or not, the
    argument can be linked using a specified *rolename*.  Field should be used
    for doc fields that usually don't occur more than once.

    The body can be linked using a specified *bodyrolename* if the content is
    just a single inline or text node.

    Example::

       :returns: description of the return value
       :rtype: description of the return type
    """
    is_grouped = False
    is_typed = False

    def __init__(self, name: str, names: tuple[str, ...]=(), label: str='', has_arg: bool=True, rolename: str='', bodyrolename: str='') -> None:
        self.name = name
        self.names = names
        self.label = label
        self.has_arg = has_arg
        self.rolename = rolename
        self.bodyrolename = bodyrolename

class GroupedField(Field):
    """
    A doc field that is grouped; i.e., all fields of that type will be
    transformed into one field with its body being a bulleted list.  It always
    has an argument.  The argument can be linked using the given *rolename*.
    GroupedField should be used for doc fields that can occur more than once.
    If *can_collapse* is true, this field will revert to a Field if only used
    once.

    Example::

       :raises ErrorClass: description when it is raised
    """
    is_grouped = True
    list_type = nodes.bullet_list

    def __init__(self, name: str, names: tuple[str, ...]=(), label: str='', rolename: str='', can_collapse: bool=False) -> None:
        super().__init__(name, names, label, True, rolename)
        self.can_collapse = can_collapse

class TypedField(GroupedField):
    """
    A doc field that is grouped and has type information for the arguments.  It
    always has an argument.  The argument can be linked using the given
    *rolename*, the type using the given *typerolename*.

    Two uses are possible: either parameter and type description are given
    separately, using a field from *names* and one from *typenames*,
    respectively, or both are given using a field from *names*, see the example.

    Example::

       :param foo: description of parameter foo
       :type foo:  SomeClass

       -- or --

       :param SomeClass foo: description of parameter foo
    """
    is_typed = True

    def __init__(self, name: str, names: tuple[str, ...]=(), typenames: tuple[str, ...]=(), label: str='', rolename: str='', typerolename: str='', can_collapse: bool=False) -> None:
        super().__init__(name, names, label, rolename, can_collapse)
        self.typenames = typenames
        self.typerolename = typerolename

class DocFieldTransformer:
    """
    Transforms field lists in "doc field" syntax into better-looking
    equivalents, using the field type definitions given on a domain.
    """
    typemap: dict[str, tuple[Field, bool]]

    def __init__(self, directive: ObjectDescription) -> None:
        self.directive = directive
        self.typemap = directive.get_field_type_map()

    def transform_all(self, node: addnodes.desc_content) -> None:
        """Transform all field list children of a node."""
        pass

    def transform(self, node: nodes.field_list) -> None:
        """Transform a single field list *node*."""
        pass