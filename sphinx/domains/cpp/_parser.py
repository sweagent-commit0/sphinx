from __future__ import annotations
import re
from typing import TYPE_CHECKING, Any
from sphinx.domains.cpp._ast import ASTAlignofExpr, ASTArray, ASTAssignmentExpr, ASTBaseClass, ASTBinOpExpr, ASTBooleanLiteral, ASTBracedInitList, ASTCastExpr, ASTCharLiteral, ASTClass, ASTCommaExpr, ASTConcept, ASTConditionalExpr, ASTDeclaration, ASTDeclarator, ASTDeclaratorMemPtr, ASTDeclaratorNameBitField, ASTDeclaratorNameParamQual, ASTDeclaratorParamPack, ASTDeclaratorParen, ASTDeclaratorPtr, ASTDeclaratorRef, ASTDeclSpecs, ASTDeclSpecsSimple, ASTDeleteExpr, ASTEnum, ASTEnumerator, ASTExplicitCast, ASTExplicitSpec, ASTExpression, ASTFallbackExpr, ASTFoldExpr, ASTFunctionParameter, ASTIdentifier, ASTIdExpression, ASTInitializer, ASTLiteral, ASTNamespace, ASTNestedName, ASTNestedNameElement, ASTNewExpr, ASTNoexceptExpr, ASTNoexceptSpec, ASTNumberLiteral, ASTOperator, ASTOperatorBuildIn, ASTOperatorLiteral, ASTOperatorType, ASTPackExpansionExpr, ASTParametersQualifiers, ASTParenExpr, ASTParenExprList, ASTPointerLiteral, ASTPostfixArray, ASTPostfixCallExpr, ASTPostfixDec, ASTPostfixExpr, ASTPostfixInc, ASTPostfixMember, ASTPostfixMemberOfPointer, ASTPostfixOp, ASTRequiresClause, ASTSizeofExpr, ASTSizeofParamPack, ASTSizeofType, ASTStringLiteral, ASTTemplateArgConstant, ASTTemplateArgs, ASTTemplateDeclarationPrefix, ASTTemplateIntroduction, ASTTemplateIntroductionParameter, ASTTemplateKeyParamPackIdDefault, ASTTemplateParam, ASTTemplateParamConstrainedTypeWithInit, ASTTemplateParamNonType, ASTTemplateParams, ASTTemplateParamTemplateType, ASTTemplateParamType, ASTThisLiteral, ASTTrailingTypeSpec, ASTTrailingTypeSpecDecltype, ASTTrailingTypeSpecDecltypeAuto, ASTTrailingTypeSpecFundamental, ASTTrailingTypeSpecName, ASTType, ASTTypeId, ASTTypeUsing, ASTTypeWithInit, ASTUnaryOpExpr, ASTUnion, ASTUserDefinedLiteral
from sphinx.domains.cpp._ids import _expression_assignment_ops, _expression_bin_ops, _expression_unary_ops, _fold_operator_re, _id_explicit_cast, _keywords, _operator_re, _simple_type_specifiers_re, _string_re, _visibility_re, udl_identifier_re
from sphinx.util import logging
from sphinx.util.cfamily import ASTAttributeList, BaseParser, DefinitionError, UnsupportedMultiCharacterCharLiteral, binary_literal_re, char_literal_re, float_literal_re, float_literal_suffix_re, hex_literal_re, identifier_re, integer_literal_re, integers_literal_suffix_re, octal_literal_re
if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
logger = logging.getLogger(__name__)

class DefinitionParser(BaseParser):

    def _parse_decl_specs_simple(self, outer: str, typed: bool) -> ASTDeclSpecsSimple:
        """Just parse the simple ones."""
        pass

    def _parse_type(self, named: bool | str, outer: str | None=None) -> ASTType:
        """
        named=False|'maybe'|True: 'maybe' is e.g., for function objects which
        doesn't need to name the arguments

        outer == operatorCast: annoying case, we should not take the params
        """
        pass