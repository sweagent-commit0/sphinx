"""Docutils node-related utility functions for Sphinx."""
from __future__ import annotations
import contextlib
import re
import unicodedata
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast
from docutils import nodes
from docutils.nodes import Node
from sphinx import addnodes
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.parsing import _fresh_title_style_context
if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator
    from docutils.nodes import Element
    from docutils.parsers.rst import Directive
    from docutils.parsers.rst.states import Inliner, RSTState
    from docutils.statemachine import StringList
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    from sphinx.util.tags import Tags
logger = logging.getLogger(__name__)
explicit_title_re = re.compile('^(.+?)\\s*(?<!\\x00)<([^<]*?)>$', re.DOTALL)
caption_ref_re = explicit_title_re
N = TypeVar('N', bound=Node)

class NodeMatcher(Generic[N]):
    """A helper class for Node.findall().

    It checks that the given node is an instance of the specified node-classes and
    has the specified node-attributes.

    For example, following example searches ``reference`` node having ``refdomain``
    and ``reftype`` attributes::

        matcher = NodeMatcher(nodes.reference, refdomain='std', reftype='citation')
        matcher.findall(doctree)
        # => [<reference ...>, <reference ...>, ...]

    A special value ``typing.Any`` matches any kind of node-attributes.  For example,
    following example searches ``reference`` node having ``refdomain`` attributes::

        matcher = NodeMatcher(nodes.reference, refdomain=Any)
        matcher.findall(doctree)
        # => [<reference ...>, <reference ...>, ...]
    """

    def __init__(self, *node_classes: type[N], **attrs: Any) -> None:
        self.classes = node_classes
        self.attrs = attrs

    def __call__(self, node: Node) -> bool:
        return self.match(node)

    def findall(self, node: Node) -> Iterator[N]:
        """An alternative to `Node.findall` with improved type safety.

        While the `NodeMatcher` object can be used as an argument to `Node.findall`, doing so
        confounds type checkers' ability to determine the return type of the iterator.
        """
        pass

def get_full_module_name(node: Node) -> str:
    """
    Return full module dotted path like: 'docutils.nodes.paragraph'

    :param nodes.Node node: target node
    :return: full module dotted path
    """
    pass

def repr_domxml(node: Node, length: int=80) -> str:
    """
    return DOM XML representation of the specified node like:
    '<paragraph translatable="False"><inline classes="versionadded">Added in version...'

    :param nodes.Node node: target node
    :param int length:
       length of return value to be striped. if false-value is specified, repr_domxml
       returns full of DOM XML representation.
    :return: DOM XML representation
    """
    pass
IGNORED_NODES = (nodes.Invisible, nodes.literal_block, nodes.doctest_block, addnodes.versionmodified)
LITERAL_TYPE_NODES = (nodes.literal_block, nodes.doctest_block, nodes.math_block, nodes.raw)
IMAGE_TYPE_NODES = (nodes.image,)

def extract_messages(doctree: Element) -> Iterable[tuple[Element, str]]:
    """Extract translatable messages from a document tree."""
    pass

def traverse_translatable_index(doctree: Element) -> Iterable[tuple[Element, list[tuple[str, str, str, str, str | None]]]]:
    """Traverse translatable index node from a document tree."""
    pass

def nested_parse_with_titles(state: RSTState, content: StringList, node: Node, content_offset: int=0) -> str:
    """Version of state.nested_parse() that allows titles and does not require
    titles to have the same decoration as the calling document.

    This is useful when the parsed content comes from a completely different
    context, such as docstrings.

    This function is retained for compatibility and will be deprecated in
    Sphinx 8. Prefer ``nested_parse_to_nodes()``.
    """
    pass

def clean_astext(node: Element) -> str:
    """Like node.astext(), but ignore images."""
    pass

def split_explicit_title(text: str) -> tuple[bool, str, str]:
    """Split role content into title and target, if given."""
    pass
indextypes = ['single', 'pair', 'double', 'triple', 'see', 'seealso']

def inline_all_toctrees(builder: Builder, docnameset: set[str], docname: str, tree: nodes.document, colorfunc: Callable[[str], str], traversed: list[str], indent: str='') -> nodes.document:
    """Inline all toctrees in the *tree*.

    Record all docnames in *docnameset*, and output docnames with *colorfunc*.
    """
    pass

def _make_id(string: str) -> str:
    """Convert `string` into an identifier and return it.

    This function is a modified version of ``docutils.nodes.make_id()`` of
    docutils-0.16.

    Changes:

    * Allow to use capital alphabet characters
    * Allow to use dots (".") and underscores ("_") for an identifier
      without a leading character.

    # Author: David Goodger <goodger@python.org>
    # Maintainer: docutils-develop@lists.sourceforge.net
    # Copyright: This module has been placed in the public domain.
    """
    pass
_non_id_chars = re.compile('[^a-zA-Z0-9._]+')
_non_id_at_ends = re.compile('^[-0-9._]+|-+$')
_non_id_translate = {248: 'o', 273: 'd', 295: 'h', 305: 'i', 322: 'l', 359: 't', 384: 'b', 387: 'b', 392: 'c', 396: 'd', 402: 'f', 409: 'k', 410: 'l', 414: 'n', 421: 'p', 427: 't', 429: 't', 436: 'y', 438: 'z', 485: 'g', 549: 'z', 564: 'l', 565: 'n', 566: 't', 567: 'j', 572: 'c', 575: 's', 576: 'z', 583: 'e', 585: 'j', 587: 'q', 589: 'r', 591: 'y'}
_non_id_translate_digraphs = {223: 'sz', 230: 'ae', 339: 'oe', 568: 'db', 569: 'qp'}

def make_id(env: BuildEnvironment, document: nodes.document, prefix: str='', term: str | None=None) -> str:
    """Generate an appropriate node_id for given *prefix* and *term*."""
    pass

def find_pending_xref_condition(node: addnodes.pending_xref, condition: str) -> Element | None:
    """Pick matched pending_xref_condition node up from the pending_xref."""
    pass

def make_refnode(builder: Builder, fromdocname: str, todocname: str, targetid: str | None, child: Node | list[Node], title: str | None=None) -> nodes.reference:
    """Shortcut to create a reference node."""
    pass
NON_SMARTQUOTABLE_PARENT_NODES = (nodes.FixedTextElement, nodes.literal, nodes.math, nodes.image, nodes.raw, nodes.problematic, addnodes.not_smartquotable)

def is_smartquotable(node: Node) -> bool:
    """Check whether the node is smart-quotable or not."""
    pass

def process_only_nodes(document: Node, tags: Tags) -> None:
    """Filter ``only`` nodes which do not match *tags*."""
    pass

def _only_node_keep_children(node: addnodes.only, tags: Tags) -> bool:
    """Keep children if tags match or error."""
    pass

def _copy_except__document(el: Element) -> Element:
    """Monkey-patch ```nodes.Element.copy``` to not copy the ``_document``
    attribute.

    xref: https://github.com/sphinx-doc/sphinx/issues/11116#issuecomment-1376767086
    """
    pass
nodes.Element.copy = _copy_except__document

def _deepcopy(el: Element) -> Element:
    """Monkey-patch ```nodes.Element.deepcopy``` for speed."""
    pass
nodes.Element.deepcopy = _deepcopy