from __future__ import annotations
from typing import TYPE_CHECKING, Any
from sphinx.domains.c._ast import ASTDeclaration, ASTIdentifier, ASTNestedName
from sphinx.locale import __
from sphinx.util import logging
if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator, Sequence
    from typing_extensions import Self
    from sphinx.environment import BuildEnvironment
logger = logging.getLogger(__name__)

class _DuplicateSymbolError(Exception):

    def __init__(self, symbol: Symbol, declaration: ASTDeclaration) -> None:
        assert symbol
        assert declaration
        self.symbol = symbol
        self.declaration = declaration

    def __str__(self) -> str:
        return 'Internal C duplicate symbol error:\n%s' % self.symbol.dump(0)

class SymbolLookupResult:

    def __init__(self, symbols: Sequence[Symbol], parentSymbol: Symbol, ident: ASTIdentifier) -> None:
        self.symbols = symbols
        self.parentSymbol = parentSymbol
        self.ident = ident

class LookupKey:

    def __init__(self, data: list[tuple[ASTIdentifier, str]]) -> None:
        self.data = data

    def __str__(self) -> str:
        inner = ', '.join((f'({ident}, {id_})' for ident, id_ in self.data))
        return f'[{inner}]'

class Symbol:
    debug_indent = 0
    debug_indent_string = '  '
    debug_lookup = False
    debug_show_tree = False

    def __copy__(self) -> Self:
        raise AssertionError

    def __deepcopy__(self, memo: Any) -> Symbol:
        if self.parent:
            raise AssertionError
        return Symbol(None, None, None, None, None)

    def __setattr__(self, key: str, value: Any) -> None:
        if key == 'children':
            raise AssertionError
        return super().__setattr__(key, value)

    def __init__(self, parent: Symbol | None, ident: ASTIdentifier | None, declaration: ASTDeclaration | None, docname: str | None, line: int | None) -> None:
        self.parent = parent
        self.siblingAbove: Symbol | None = None
        self.siblingBelow: Symbol | None = None
        self.ident = ident
        self.declaration = declaration
        self.docname = docname
        self.line = line
        self.isRedeclaration = False
        self._assert_invariants()
        self._children_by_name: dict[str, Symbol] = {}
        self._children_by_docname: dict[str, dict[str, Symbol]] = {}
        self._anon_children: set[Symbol] = set()
        if self.parent:
            self.parent._add_child(self)
        if self.declaration:
            self.declaration.symbol = self
        self._add_function_params()

    def __repr__(self) -> str:
        return f'<Symbol {self.to_string(indent=0)!r}>'