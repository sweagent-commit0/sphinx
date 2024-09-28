"""Utility functions common to the C and C++ domains."""
from __future__ import annotations
import re
from copy import deepcopy
from typing import TYPE_CHECKING
from docutils import nodes
from sphinx import addnodes
from sphinx.util import logging
if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from typing import Any, TypeAlias
    from docutils.nodes import TextElement
    from sphinx.config import Config
    StringifyTransform: TypeAlias = Callable[[Any], str]
logger = logging.getLogger(__name__)
_whitespace_re = re.compile('\\s+')
anon_identifier_re = re.compile('(@[a-zA-Z0-9_])[a-zA-Z0-9_]*\\b')
identifier_re = re.compile("\n    (   # This 'extends' _anon_identifier_re with the ordinary identifiers,\n        # make sure they are in sync.\n        (~?\\b[a-zA-Z_])  # ordinary identifiers\n    |   (@[a-zA-Z0-9_])  # our extension for names of anonymous entities\n    )\n    [a-zA-Z0-9_]*\\b\n", flags=re.VERBOSE)
integer_literal_re = re.compile("[1-9][0-9]*(\\'[0-9]+)*")
octal_literal_re = re.compile("0[0-7]*(\\'[0-7]+)*")
hex_literal_re = re.compile("0[xX][0-9a-fA-F]+(\\'[0-9a-fA-F]+)*")
binary_literal_re = re.compile("0[bB][01]+(\\'[01]+)*")
integers_literal_suffix_re = re.compile('\n    # unsigned and/or (long) long, in any order, but at least one of them\n    (\n        ([uU]    ([lL]  |  (ll)  |  (LL))?)\n        |\n        (([lL]  |  (ll)  |  (LL))    [uU]?)\n    )\\b\n    # the ending word boundary is important for distinguishing\n    # between suffixes and UDLs in C++\n', flags=re.VERBOSE)
float_literal_re = re.compile("\n    [+-]?(\n    # decimal\n      ([0-9]+(\\'[0-9]+)*[eE][+-]?[0-9]+(\\'[0-9]+)*)\n    | (([0-9]+(\\'[0-9]+)*)?\\.[0-9]+(\\'[0-9]+)*([eE][+-]?[0-9]+(\\'[0-9]+)*)?)\n    | ([0-9]+(\\'[0-9]+)*\\.([eE][+-]?[0-9]+(\\'[0-9]+)*)?)\n    # hex\n    | (0[xX][0-9a-fA-F]+(\\'[0-9a-fA-F]+)*[pP][+-]?[0-9a-fA-F]+(\\'[0-9a-fA-F]+)*)\n    | (0[xX]([0-9a-fA-F]+(\\'[0-9a-fA-F]+)*)?\\.\n        [0-9a-fA-F]+(\\'[0-9a-fA-F]+)*([pP][+-]?[0-9a-fA-F]+(\\'[0-9a-fA-F]+)*)?)\n    | (0[xX][0-9a-fA-F]+(\\'[0-9a-fA-F]+)*\\.([pP][+-]?[0-9a-fA-F]+(\\'[0-9a-fA-F]+)*)?)\n    )\n", flags=re.VERBOSE)
float_literal_suffix_re = re.compile('[fFlL]\\b')
char_literal_re = re.compile('\n    ((?:u8)|u|U|L)?\n    \'(\n      (?:[^\\\\\'])\n    | (\\\\(\n        (?:[\'"?\\\\abfnrtv])\n      | (?:[0-7]{1,3})\n      | (?:x[0-9a-fA-F]{2})\n      | (?:u[0-9a-fA-F]{4})\n      | (?:U[0-9a-fA-F]{8})\n      ))\n    )\'\n', flags=re.VERBOSE)

class NoOldIdError(Exception):
    pass

class ASTBaseBase:

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __str__(self) -> str:
        return self._stringify(str)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self._stringify(repr)}>'

class ASTAttribute(ASTBaseBase):
    pass

class ASTCPPAttribute(ASTAttribute):

    def __init__(self, arg: str) -> None:
        self.arg = arg

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTCPPAttribute):
            return NotImplemented
        return self.arg == other.arg

    def __hash__(self) -> int:
        return hash(self.arg)

class ASTGnuAttribute(ASTBaseBase):

    def __init__(self, name: str, args: ASTBaseParenExprList | None) -> None:
        self.name = name
        self.args = args

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTGnuAttribute):
            return NotImplemented
        return self.name == other.name and self.args == other.args

    def __hash__(self) -> int:
        return hash((self.name, self.args))

class ASTGnuAttributeList(ASTAttribute):

    def __init__(self, attrs: list[ASTGnuAttribute]) -> None:
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTGnuAttributeList):
            return NotImplemented
        return self.attrs == other.attrs

    def __hash__(self) -> int:
        return hash(self.attrs)

class ASTIdAttribute(ASTAttribute):
    """For simple attributes defined by the user."""

    def __init__(self, id: str) -> None:
        self.id = id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTIdAttribute):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

class ASTParenAttribute(ASTAttribute):
    """For paren attributes defined by the user."""

    def __init__(self, id: str, arg: str) -> None:
        self.id = id
        self.arg = arg

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTParenAttribute):
            return NotImplemented
        return self.id == other.id and self.arg == other.arg

    def __hash__(self) -> int:
        return hash((self.id, self.arg))

class ASTAttributeList(ASTBaseBase):

    def __init__(self, attrs: list[ASTAttribute]) -> None:
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTAttributeList):
            return NotImplemented
        return self.attrs == other.attrs

    def __hash__(self) -> int:
        return hash(self.attrs)

    def __len__(self) -> int:
        return len(self.attrs)

    def __add__(self, other: ASTAttributeList) -> ASTAttributeList:
        return ASTAttributeList(self.attrs + other.attrs)

class ASTBaseParenExprList(ASTBaseBase):
    pass

class UnsupportedMultiCharacterCharLiteral(Exception):
    pass

class DefinitionError(Exception):
    pass

class BaseParser:

    def __init__(self, definition: str, *, location: nodes.Node | tuple[str, int] | str, config: Config) -> None:
        self.definition = definition.strip()
        self.location = location
        self.config = config
        self.pos = 0
        self.end = len(self.definition)
        self.last_match: re.Match[str] | None = None
        self._previous_state: tuple[int, re.Match[str] | None] = (0, None)
        self.otherErrors: list[DefinitionError] = []
        self.allowFallbackExpressionParsing = True