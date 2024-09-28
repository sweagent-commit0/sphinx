from __future__ import annotations
from typing import TYPE_CHECKING, Any
from sphinx.domains.c._ast import ASTAlignofExpr, ASTArray, ASTAssignmentExpr, ASTBinOpExpr, ASTBooleanLiteral, ASTBracedInitList, ASTCastExpr, ASTCharLiteral, ASTDeclaration, ASTDeclarator, ASTDeclaratorNameBitField, ASTDeclaratorNameParam, ASTDeclaratorParen, ASTDeclaratorPtr, ASTDeclSpecs, ASTDeclSpecsSimple, ASTEnum, ASTEnumerator, ASTExpression, ASTFallbackExpr, ASTFunctionParameter, ASTIdentifier, ASTIdExpression, ASTInitializer, ASTLiteral, ASTMacro, ASTMacroParameter, ASTNestedName, ASTNumberLiteral, ASTParameters, ASTParenExpr, ASTParenExprList, ASTPostfixArray, ASTPostfixCallExpr, ASTPostfixDec, ASTPostfixExpr, ASTPostfixInc, ASTPostfixMemberOfPointer, ASTPostfixOp, ASTSizeofExpr, ASTSizeofType, ASTStringLiteral, ASTStruct, ASTTrailingTypeSpec, ASTTrailingTypeSpecFundamental, ASTTrailingTypeSpecName, ASTType, ASTTypeWithInit, ASTUnaryOpExpr, ASTUnion
from sphinx.domains.c._ids import _expression_assignment_ops, _expression_bin_ops, _expression_unary_ops, _keywords, _simple_type_specifiers_re, _string_re
from sphinx.util.cfamily import ASTAttributeList, BaseParser, DefinitionError, UnsupportedMultiCharacterCharLiteral, binary_literal_re, char_literal_re, float_literal_re, float_literal_suffix_re, hex_literal_re, identifier_re, integer_literal_re, integers_literal_suffix_re, octal_literal_re
if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from sphinx.domains.c._ast import DeclarationType

class DefinitionParser(BaseParser):

    def _parse_decl_specs_simple(self, outer: str | None, typed: bool) -> ASTDeclSpecsSimple:
        """Just parse the simple ones."""
        pass

    def _parse_type(self, named: bool | str, outer: str | None=None) -> ASTType:
        """
        named=False|'single'|True: 'single' is e.g., for function objects which
        doesn't need to name the arguments, but otherwise is a single name
        """
        pass