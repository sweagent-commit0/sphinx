"""Index entries adapters for sphinx.environment."""
from __future__ import annotations
import re
import unicodedata
from itertools import groupby
from typing import TYPE_CHECKING
from sphinx.errors import NoUri
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.index_entries import _split_into
if TYPE_CHECKING:
    from typing import Literal, TypeAlias
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    _IndexEntryTarget: TypeAlias = tuple[str | None, str | Literal[False]]
    _IndexEntryTargets: TypeAlias = list[_IndexEntryTarget]
    _IndexEntryCategoryKey: TypeAlias = str | None
    _IndexEntrySubItems: TypeAlias = dict[str, tuple[_IndexEntryTargets, _IndexEntryCategoryKey]]
    _IndexEntry: TypeAlias = tuple[_IndexEntryTargets, _IndexEntrySubItems, _IndexEntryCategoryKey]
    _IndexEntryMap: TypeAlias = dict[str, _IndexEntry]
    _Index: TypeAlias = list[tuple[str, list[tuple[str, tuple[_IndexEntryTargets, list[tuple[str, _IndexEntryTargets]], _IndexEntryCategoryKey]]]]]
logger = logging.getLogger(__name__)

class IndexEntries:

    def __init__(self, env: BuildEnvironment) -> None:
        self.env = env
        self.builder: Builder

    def create_index(self, builder: Builder, group_entries: bool=True, _fixre: re.Pattern[str]=re.compile('(.*) ([(][^()]*[)])')) -> _Index:
        """Create the real index from the collected index entries."""
        pass

def _key_func_0(entry: _IndexEntryTarget) -> tuple[bool, str | Literal[False]]:
    """Sort the index entries for same keyword."""
    pass

def _key_func_1(entry: tuple[str, _IndexEntry]) -> tuple[tuple[int, str], str]:
    """Sort the index entries"""
    pass

def _key_func_2(entry: tuple[str, _IndexEntryTargets]) -> str:
    """Sort the sub-index entries"""
    pass

def _group_by_func(entry: tuple[str, _IndexEntry]) -> str:
    """Group the entries by letter or category key."""
    pass