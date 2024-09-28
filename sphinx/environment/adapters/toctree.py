"""Toctree adapter for sphinx.environment."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, TypeVar
from docutils import nodes
from docutils.nodes import Element, Node
from sphinx import addnodes
from sphinx.locale import __
from sphinx.util import logging, url_re
from sphinx.util.matching import Matcher
from sphinx.util.nodes import _only_node_keep_children, clean_astext
if TYPE_CHECKING:
    from collections.abc import Iterable, Set
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    from sphinx.util.tags import Tags
logger = logging.getLogger(__name__)

def note_toctree(env: BuildEnvironment, docname: str, toctreenode: addnodes.toctree) -> None:
    """Note a TOC tree directive in a document and gather information about
    file relations from it.
    """
    pass

def document_toc(env: BuildEnvironment, docname: str, tags: Tags) -> Node:
    """Get the (local) table of contents for a document.

    Note that this is only the sections within the document.
    For a ToC tree that shows the document's place in the
    ToC structure, use `get_toctree_for`.
    """
    pass

def global_toctree_for_doc(env: BuildEnvironment, docname: str, builder: Builder, collapse: bool=False, includehidden: bool=True, maxdepth: int=0, titles_only: bool=False) -> Element | None:
    """Get the global ToC tree at a given document.

    This gives the global ToC, with all ancestors and their siblings.
    """
    pass

def _resolve_toctree(env: BuildEnvironment, docname: str, builder: Builder, toctree: addnodes.toctree, *, prune: bool=True, maxdepth: int=0, titles_only: bool=False, collapse: bool=False, includehidden: bool=False) -> Element | None:
    """Resolve a *toctree* node into individual bullet lists with titles
    as items, returning None (if no containing titles are found) or
    a new node.

    If *prune* is True, the tree is pruned to *maxdepth*, or if that is 0,
    to the value of the *maxdepth* option on the *toctree* node.
    If *titles_only* is True, only toplevel document titles will be in the
    resulting tree.
    If *collapse* is True, all branches not containing docname will
    be collapsed.
    """
    pass

def _entries_from_toctree(env: BuildEnvironment, prune: bool, titles_only: bool, collapse: bool, includehidden: bool, tags: Tags, toctree_ancestors: Set[str], included: Matcher, excluded: Matcher, toctreenode: addnodes.toctree, parents: list[str], subtree: bool=False) -> list[Element]:
    """Return TOC entries for a toctree node."""
    pass

def _toctree_add_classes(node: Element, depth: int, docname: str) -> None:
    """Add 'toctree-l%d' and 'current' classes to the toctree."""
    pass
ET = TypeVar('ET', bound=Element)

def _toctree_copy(node: ET, depth: int, maxdepth: int, collapse: bool, tags: Tags) -> ET:
    """Utility: Cut and deep-copy a TOC at a specified depth."""
    pass

class TocTree:

    def __init__(self, env: BuildEnvironment) -> None:
        self.env = env