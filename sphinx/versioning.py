"""Implements the low-level algorithms Sphinx uses for versioning doctrees."""
from __future__ import annotations
import pickle
from itertools import product, zip_longest
from operator import itemgetter
from os import path
from typing import TYPE_CHECKING, Any
from uuid import uuid4
from sphinx.transforms import SphinxTransform
if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
try:
    import Levenshtein
    IS_SPEEDUP = True
except ImportError:
    IS_SPEEDUP = False
VERSIONING_RATIO = 65

def add_uids(doctree: Node, condition: Callable[[Node], bool]) -> Iterator[Node]:
    """Add a unique id to every node in the `doctree` which matches the
    condition and yield the nodes.

    :param doctree:
        A :class:`docutils.nodes.document` instance.

    :param condition:
        A callable which returns either ``True`` or ``False`` for a given node.
    """
    pass

def merge_doctrees(old: Node, new: Node, condition: Callable[[Node], bool]) -> Iterator[Node]:
    """Merge the `old` doctree with the `new` one while looking at nodes
    matching the `condition`.

    Each node which replaces another one or has been added to the `new` doctree
    will be yielded.

    :param condition:
        A callable which returns either ``True`` or ``False`` for a given node.
    """
    pass

def get_ratio(old: str, new: str) -> float:
    """Return a "similarity ratio" (in percent) representing the similarity
    between the two strings where 0 is equal and anything above less than equal.
    """
    pass

def levenshtein_distance(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between two strings *a* and *b*."""
    pass

class UIDTransform(SphinxTransform):
    """Add UIDs to doctree for versioning."""
    default_priority = 880