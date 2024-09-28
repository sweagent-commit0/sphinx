from __future__ import annotations
import warnings
from typing import TYPE_CHECKING
import jinja2.environment
import jinja2.nodes
import jinja2.parser
from sphinx.deprecation import RemovedInSphinx90Warning
if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
    from typing import Literal
_ENV = jinja2.environment.Environment()

class BooleanParser(jinja2.parser.Parser):
    """Only allow conditional expressions and binary operators."""

class Tags:

    def __init__(self, tags: Sequence[str]=()) -> None:
        self._tags = set(tags or ())
        self._condition_cache: dict[str, bool] = {}

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({', '.join(sorted(self._tags))})'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({tuple(sorted(self._tags))})'

    def __iter__(self) -> Iterator[str]:
        return iter(self._tags)

    def __contains__(self, tag: str) -> bool:
        return tag in self._tags

    def eval_condition(self, condition: str) -> bool:
        """Evaluate a boolean condition.

        Only conditional expressions and binary operators (and, or, not)
        are permitted, and operate on tag names, where truthy values mean
        the tag is present and vice versa.
        """
        pass