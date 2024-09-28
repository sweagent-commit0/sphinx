from __future__ import annotations
from typing import TYPE_CHECKING, Any, NoReturn
from sphinx.domains.cpp._ast import ASTDeclaration, ASTIdentifier, ASTNestedName, ASTNestedNameElement, ASTOperator, ASTTemplateArgs, ASTTemplateDeclarationPrefix, ASTTemplateIntroduction, ASTTemplateParams
from sphinx.locale import __
from sphinx.util import logging
if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from sphinx.environment import BuildEnvironment
logger = logging.getLogger(__name__)

class _DuplicateSymbolError(Exception):

    def __init__(self, symbol: Symbol, declaration: ASTDeclaration) -> None:
        assert symbol
        assert declaration
        self.symbol = symbol
        self.declaration = declaration

    def __str__(self) -> str:
        return 'Internal C++ duplicate symbol error:\n%s' % self.symbol.dump(0)

class SymbolLookupResult:

    def __init__(self, symbols: Iterator[Symbol], parentSymbol: Symbol, identOrOp: ASTIdentifier | ASTOperator, templateParams: Any, templateArgs: ASTTemplateArgs) -> None:
        self.symbols = symbols
        self.parentSymbol = parentSymbol
        self.identOrOp = identOrOp
        self.templateParams = templateParams
        self.templateArgs = templateArgs

class LookupKey:

    def __init__(self, data: list[tuple[ASTNestedNameElement, ASTTemplateParams | ASTTemplateIntroduction, str]]) -> None:
        self.data = data

class Symbol:
    debug_indent = 0
    debug_indent_string = '  '
    debug_lookup = False
    debug_show_tree = False

    def __copy__(self) -> NoReturn:
        raise AssertionError

    def __deepcopy__(self, memo: Any) -> Symbol:
        if self.parent:
            raise AssertionError
        return Symbol(None, None, None, None, None, None, None)

    def __setattr__(self, key: str, value: Any) -> None:
        if key == 'children':
            raise AssertionError
        return super().__setattr__(key, value)

    def __init__(self, parent: Symbol | None, identOrOp: ASTIdentifier | ASTOperator | None, templateParams: ASTTemplateParams | ASTTemplateIntroduction | None, templateArgs: Any, declaration: ASTDeclaration | None, docname: str | None, line: int | None) -> None:
        self.parent = parent
        self.siblingAbove: Symbol | None = None
        self.siblingBelow: Symbol | None = None
        self.identOrOp = identOrOp
        if templateArgs is not None and (not _is_specialization(templateParams, templateArgs)):
            templateArgs = None
        self.templateParams = templateParams
        self.templateArgs = templateArgs
        self.declaration = declaration
        self.docname = docname
        self.line = line
        self.isRedeclaration = False
        self._assert_invariants()
        self._children: list[Symbol] = []
        self._anonChildren: list[Symbol] = []
        if self.parent:
            self.parent._children.append(self)
        if self.declaration:
            self.declaration.symbol = self
        self._add_template_and_function_params()

    def __repr__(self) -> str:
        return f'<Symbol {self.to_string(indent=0)!r}>'