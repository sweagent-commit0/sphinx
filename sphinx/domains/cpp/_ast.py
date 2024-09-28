from __future__ import annotations
import sys
import warnings
from typing import TYPE_CHECKING, Any, ClassVar, Literal
from docutils import nodes
from sphinx import addnodes
from sphinx.domains.cpp._ids import _id_char_from_prefix, _id_explicit_cast, _id_fundamental_v1, _id_fundamental_v2, _id_operator_unary_v2, _id_operator_v1, _id_operator_v2, _id_prefix, _id_shorthands_v1, _max_id
from sphinx.util.cfamily import ASTAttributeList, ASTBaseBase, ASTBaseParenExprList, NoOldIdError, UnsupportedMultiCharacterCharLiteral, verify_description_mode
if TYPE_CHECKING:
    from docutils.nodes import Element, TextElement
    from sphinx.addnodes import desc_signature
    from sphinx.domains.cpp._symbol import Symbol
    from sphinx.environment import BuildEnvironment
    from sphinx.util.cfamily import StringifyTransform

class ASTBase(ASTBaseBase):
    pass

class ASTIdentifier(ASTBase):

    def __init__(self, name: str) -> None:
        if not isinstance(name, str) or len(name) == 0:
            raise AssertionError
        self.name = sys.intern(name)
        self.is_anonymous = name[0] == '@'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTIdentifier):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name

class ASTNestedNameElement(ASTBase):

    def __init__(self, identOrOp: ASTIdentifier | ASTOperator, templateArgs: ASTTemplateArgs | None) -> None:
        self.identOrOp = identOrOp
        self.templateArgs = templateArgs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTNestedNameElement):
            return NotImplemented
        return self.identOrOp == other.identOrOp and self.templateArgs == other.templateArgs

    def __hash__(self) -> int:
        return hash((self.identOrOp, self.templateArgs))

class ASTNestedName(ASTBase):

    def __init__(self, names: list[ASTNestedNameElement], templates: list[bool], rooted: bool) -> None:
        assert len(names) > 0
        self.names = names
        self.templates = templates
        assert len(self.names) == len(self.templates)
        self.rooted = rooted

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTNestedName):
            return NotImplemented
        return self.names == other.names and self.templates == other.templates and (self.rooted == other.rooted)

    def __hash__(self) -> int:
        return hash((self.names, self.templates, self.rooted))

class ASTExpression(ASTBase):
    pass

class ASTLiteral(ASTExpression):
    pass

class ASTPointerLiteral(ASTLiteral):

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ASTPointerLiteral)

    def __hash__(self) -> int:
        return hash('nullptr')

class ASTBooleanLiteral(ASTLiteral):

    def __init__(self, value: bool) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTBooleanLiteral):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

class ASTNumberLiteral(ASTLiteral):

    def __init__(self, data: str) -> None:
        self.data = data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTNumberLiteral):
            return NotImplemented
        return self.data == other.data

    def __hash__(self) -> int:
        return hash(self.data)

class ASTStringLiteral(ASTLiteral):

    def __init__(self, data: str) -> None:
        self.data = data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTStringLiteral):
            return NotImplemented
        return self.data == other.data

    def __hash__(self) -> int:
        return hash(self.data)

class ASTCharLiteral(ASTLiteral):

    def __init__(self, prefix: str, data: str) -> None:
        self.prefix = prefix
        self.data = data
        assert prefix in _id_char_from_prefix
        self.type = _id_char_from_prefix[prefix]
        decoded = data.encode().decode('unicode-escape')
        if len(decoded) == 1:
            self.value = ord(decoded)
        else:
            raise UnsupportedMultiCharacterCharLiteral(decoded)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTCharLiteral):
            return NotImplemented
        return self.prefix == other.prefix and self.value == other.value

    def __hash__(self) -> int:
        return hash((self.prefix, self.value))

class ASTUserDefinedLiteral(ASTLiteral):

    def __init__(self, literal: ASTLiteral, ident: ASTIdentifier) -> None:
        self.literal = literal
        self.ident = ident

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTUserDefinedLiteral):
            return NotImplemented
        return self.literal == other.literal and self.ident == other.ident

    def __hash__(self) -> int:
        return hash((self.literal, self.ident))

class ASTThisLiteral(ASTExpression):

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ASTThisLiteral)

    def __hash__(self) -> int:
        return hash('this')

class ASTFoldExpr(ASTExpression):

    def __init__(self, leftExpr: ASTExpression | None, op: str, rightExpr: ASTExpression | None) -> None:
        assert leftExpr is not None or rightExpr is not None
        self.leftExpr = leftExpr
        self.op = op
        self.rightExpr = rightExpr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTFoldExpr):
            return NotImplemented
        return self.leftExpr == other.leftExpr and self.op == other.op and (self.rightExpr == other.rightExpr)

    def __hash__(self) -> int:
        return hash((self.leftExpr, self.op, self.rightExpr))

class ASTParenExpr(ASTExpression):

    def __init__(self, expr: ASTExpression) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTParenExpr):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTIdExpression(ASTExpression):

    def __init__(self, name: ASTNestedName) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTIdExpression):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

class ASTPostfixOp(ASTBase):
    pass

class ASTPostfixArray(ASTPostfixOp):

    def __init__(self, expr: ASTExpression) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTPostfixArray):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTPostfixMember(ASTPostfixOp):

    def __init__(self, name: ASTNestedName) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTPostfixMember):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

class ASTPostfixMemberOfPointer(ASTPostfixOp):

    def __init__(self, name: ASTNestedName) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTPostfixMemberOfPointer):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

class ASTPostfixInc(ASTPostfixOp):

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ASTPostfixInc)

    def __hash__(self) -> int:
        return hash('++')

class ASTPostfixDec(ASTPostfixOp):

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ASTPostfixDec)

    def __hash__(self) -> int:
        return hash('--')

class ASTPostfixCallExpr(ASTPostfixOp):

    def __init__(self, lst: ASTParenExprList | ASTBracedInitList) -> None:
        self.lst = lst

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTPostfixCallExpr):
            return NotImplemented
        return self.lst == other.lst

    def __hash__(self) -> int:
        return hash(self.lst)

class ASTPostfixExpr(ASTExpression):

    def __init__(self, prefix: ASTType, postFixes: list[ASTPostfixOp]) -> None:
        self.prefix = prefix
        self.postFixes = postFixes

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTPostfixExpr):
            return NotImplemented
        return self.prefix == other.prefix and self.postFixes == other.postFixes

    def __hash__(self) -> int:
        return hash((self.prefix, self.postFixes))

class ASTExplicitCast(ASTExpression):

    def __init__(self, cast: str, typ: ASTType, expr: ASTExpression) -> None:
        assert cast in _id_explicit_cast
        self.cast = cast
        self.typ = typ
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTExplicitCast):
            return NotImplemented
        return self.cast == other.cast and self.typ == other.typ and (self.expr == other.expr)

    def __hash__(self) -> int:
        return hash((self.cast, self.typ, self.expr))

class ASTTypeId(ASTExpression):

    def __init__(self, typeOrExpr: ASTType | ASTExpression, isType: bool) -> None:
        self.typeOrExpr = typeOrExpr
        self.isType = isType

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTypeId):
            return NotImplemented
        return self.typeOrExpr == other.typeOrExpr and self.isType == other.isType

    def __hash__(self) -> int:
        return hash((self.typeOrExpr, self.isType))

class ASTUnaryOpExpr(ASTExpression):

    def __init__(self, op: str, expr: ASTExpression) -> None:
        self.op = op
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTUnaryOpExpr):
            return NotImplemented
        return self.op == other.op and self.expr == other.expr

    def __hash__(self) -> int:
        return hash((self.op, self.expr))

class ASTSizeofParamPack(ASTExpression):

    def __init__(self, identifier: ASTIdentifier) -> None:
        self.identifier = identifier

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTSizeofParamPack):
            return NotImplemented
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)

class ASTSizeofType(ASTExpression):

    def __init__(self, typ: ASTType) -> None:
        self.typ = typ

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTSizeofType):
            return NotImplemented
        return self.typ == other.typ

    def __hash__(self) -> int:
        return hash(self.typ)

class ASTSizeofExpr(ASTExpression):

    def __init__(self, expr: ASTExpression) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTSizeofExpr):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTAlignofExpr(ASTExpression):

    def __init__(self, typ: ASTType) -> None:
        self.typ = typ

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTAlignofExpr):
            return NotImplemented
        return self.typ == other.typ

    def __hash__(self) -> int:
        return hash(self.typ)

class ASTNoexceptExpr(ASTExpression):

    def __init__(self, expr: ASTExpression) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTNoexceptExpr):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTNewExpr(ASTExpression):

    def __init__(self, rooted: bool, isNewTypeId: bool, typ: ASTType, initList: ASTParenExprList | ASTBracedInitList) -> None:
        self.rooted = rooted
        self.isNewTypeId = isNewTypeId
        self.typ = typ
        self.initList = initList

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTNewExpr):
            return NotImplemented
        return self.rooted == other.rooted and self.isNewTypeId == other.isNewTypeId and (self.typ == other.typ) and (self.initList == other.initList)

    def __hash__(self) -> int:
        return hash((self.rooted, self.isNewTypeId, self.typ, self.initList))

class ASTDeleteExpr(ASTExpression):

    def __init__(self, rooted: bool, array: bool, expr: ASTExpression) -> None:
        self.rooted = rooted
        self.array = array
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeleteExpr):
            return NotImplemented
        return self.rooted == other.rooted and self.array == other.array and (self.expr == other.expr)

    def __hash__(self) -> int:
        return hash((self.rooted, self.array, self.expr))

class ASTCastExpr(ASTExpression):

    def __init__(self, typ: ASTType, expr: ASTExpression) -> None:
        self.typ = typ
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTCastExpr):
            return NotImplemented
        return self.typ == other.typ and self.expr == other.expr

    def __hash__(self) -> int:
        return hash((self.typ, self.expr))

class ASTBinOpExpr(ASTExpression):

    def __init__(self, exprs: list[ASTExpression], ops: list[str]) -> None:
        assert len(exprs) > 0
        assert len(exprs) == len(ops) + 1
        self.exprs = exprs
        self.ops = ops

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTBinOpExpr):
            return NotImplemented
        return self.exprs == other.exprs and self.ops == other.ops

    def __hash__(self) -> int:
        return hash((self.exprs, self.ops))

class ASTConditionalExpr(ASTExpression):

    def __init__(self, ifExpr: ASTExpression, thenExpr: ASTExpression, elseExpr: ASTExpression) -> None:
        self.ifExpr = ifExpr
        self.thenExpr = thenExpr
        self.elseExpr = elseExpr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTConditionalExpr):
            return NotImplemented
        return self.ifExpr == other.ifExpr and self.thenExpr == other.thenExpr and (self.elseExpr == other.elseExpr)

    def __hash__(self) -> int:
        return hash((self.ifExpr, self.thenExpr, self.elseExpr))

class ASTBracedInitList(ASTBase):

    def __init__(self, exprs: list[ASTExpression | ASTBracedInitList], trailingComma: bool) -> None:
        self.exprs = exprs
        self.trailingComma = trailingComma

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTBracedInitList):
            return NotImplemented
        return self.exprs == other.exprs and self.trailingComma == other.trailingComma

    def __hash__(self) -> int:
        return hash((self.exprs, self.trailingComma))

class ASTAssignmentExpr(ASTExpression):

    def __init__(self, leftExpr: ASTExpression, op: str, rightExpr: ASTExpression | ASTBracedInitList) -> None:
        self.leftExpr = leftExpr
        self.op = op
        self.rightExpr = rightExpr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTAssignmentExpr):
            return NotImplemented
        return self.leftExpr == other.leftExpr and self.op == other.op and (self.rightExpr == other.rightExpr)

    def __hash__(self) -> int:
        return hash((self.leftExpr, self.op, self.rightExpr))

class ASTCommaExpr(ASTExpression):

    def __init__(self, exprs: list[ASTExpression]) -> None:
        assert len(exprs) > 0
        self.exprs = exprs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTCommaExpr):
            return NotImplemented
        return self.exprs == other.exprs

    def __hash__(self) -> int:
        return hash(self.exprs)

class ASTFallbackExpr(ASTExpression):

    def __init__(self, expr: str) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTFallbackExpr):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTOperator(ASTBase):
    is_anonymous: ClassVar[Literal[False]] = False

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError(repr(self))

    def __hash__(self) -> int:
        raise NotImplementedError(repr(self))

    def _describe_identifier(self, signode: TextElement, identnode: TextElement, env: BuildEnvironment, symbol: Symbol) -> None:
        """Render the prefix into signode, and the last part into identnode."""
        pass

class ASTOperatorBuildIn(ASTOperator):

    def __init__(self, op: str) -> None:
        self.op = op

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTOperatorBuildIn):
            return NotImplemented
        return self.op == other.op

    def __hash__(self) -> int:
        return hash(self.op)

class ASTOperatorLiteral(ASTOperator):

    def __init__(self, identifier: ASTIdentifier) -> None:
        self.identifier = identifier

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTOperatorLiteral):
            return NotImplemented
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)

class ASTOperatorType(ASTOperator):

    def __init__(self, type: ASTType) -> None:
        self.type = type

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTOperatorType):
            return NotImplemented
        return self.type == other.type

    def __hash__(self) -> int:
        return hash(self.type)

class ASTTemplateArgConstant(ASTBase):

    def __init__(self, value: ASTExpression) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTemplateArgConstant):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

class ASTTemplateArgs(ASTBase):

    def __init__(self, args: list[ASTType | ASTTemplateArgConstant], packExpansion: bool) -> None:
        assert args is not None
        self.args = args
        self.packExpansion = packExpansion

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTemplateArgs):
            return NotImplemented
        return self.args == other.args and self.packExpansion == other.packExpansion

    def __hash__(self) -> int:
        return hash((self.args, self.packExpansion))

class ASTTrailingTypeSpec(ASTBase):
    pass

class ASTTrailingTypeSpecFundamental(ASTTrailingTypeSpec):

    def __init__(self, names: list[str], canonNames: list[str]) -> None:
        assert len(names) != 0
        assert len(names) == len(canonNames), (names, canonNames)
        self.names = names
        self.canonNames = canonNames

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTrailingTypeSpecFundamental):
            return NotImplemented
        return self.names == other.names and self.canonNames == other.canonNames

    def __hash__(self) -> int:
        return hash((self.names, self.canonNames))

class ASTTrailingTypeSpecDecltypeAuto(ASTTrailingTypeSpec):

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ASTTrailingTypeSpecDecltypeAuto)

    def __hash__(self) -> int:
        return hash('decltype(auto)')

class ASTTrailingTypeSpecDecltype(ASTTrailingTypeSpec):

    def __init__(self, expr: ASTExpression) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTrailingTypeSpecDecltype):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTTrailingTypeSpecName(ASTTrailingTypeSpec):

    def __init__(self, prefix: str, nestedName: ASTNestedName, placeholderType: str | None) -> None:
        self.prefix = prefix
        self.nestedName = nestedName
        self.placeholderType = placeholderType

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTrailingTypeSpecName):
            return NotImplemented
        return self.prefix == other.prefix and self.nestedName == other.nestedName and (self.placeholderType == other.placeholderType)

    def __hash__(self) -> int:
        return hash((self.prefix, self.nestedName, self.placeholderType))

class ASTFunctionParameter(ASTBase):

    def __init__(self, arg: ASTTypeWithInit | ASTTemplateParamConstrainedTypeWithInit, ellipsis: bool=False) -> None:
        self.arg = arg
        self.ellipsis = ellipsis

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTFunctionParameter):
            return NotImplemented
        return self.arg == other.arg and self.ellipsis == other.ellipsis

    def __hash__(self) -> int:
        return hash((self.arg, self.ellipsis))

class ASTNoexceptSpec(ASTBase):

    def __init__(self, expr: ASTExpression | None) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTNoexceptSpec):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTParametersQualifiers(ASTBase):

    def __init__(self, args: list[ASTFunctionParameter], volatile: bool, const: bool, refQual: str | None, exceptionSpec: ASTNoexceptSpec, trailingReturn: ASTType, override: bool, final: bool, attrs: ASTAttributeList, initializer: str | None) -> None:
        self.args = args
        self.volatile = volatile
        self.const = const
        self.refQual = refQual
        self.exceptionSpec = exceptionSpec
        self.trailingReturn = trailingReturn
        self.override = override
        self.final = final
        self.attrs = attrs
        self.initializer = initializer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTParametersQualifiers):
            return NotImplemented
        return self.args == other.args and self.volatile == other.volatile and (self.const == other.const) and (self.refQual == other.refQual) and (self.exceptionSpec == other.exceptionSpec) and (self.trailingReturn == other.trailingReturn) and (self.override == other.override) and (self.final == other.final) and (self.attrs == other.attrs) and (self.initializer == other.initializer)

    def __hash__(self) -> int:
        return hash((self.args, self.volatile, self.const, self.refQual, self.exceptionSpec, self.trailingReturn, self.override, self.final, self.attrs, self.initializer))

class ASTExplicitSpec(ASTBase):

    def __init__(self, expr: ASTExpression | None) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTExplicitSpec):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTDeclSpecsSimple(ASTBase):

    def __init__(self, storage: str, threadLocal: bool, inline: bool, virtual: bool, explicitSpec: ASTExplicitSpec | None, consteval: bool, constexpr: bool, constinit: bool, volatile: bool, const: bool, friend: bool, attrs: ASTAttributeList) -> None:
        self.storage = storage
        self.threadLocal = threadLocal
        self.inline = inline
        self.virtual = virtual
        self.explicitSpec = explicitSpec
        self.consteval = consteval
        self.constexpr = constexpr
        self.constinit = constinit
        self.volatile = volatile
        self.const = const
        self.friend = friend
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclSpecsSimple):
            return NotImplemented
        return self.storage == other.storage and self.threadLocal == other.threadLocal and (self.inline == other.inline) and (self.virtual == other.virtual) and (self.explicitSpec == other.explicitSpec) and (self.consteval == other.consteval) and (self.constexpr == other.constexpr) and (self.constinit == other.constinit) and (self.volatile == other.volatile) and (self.const == other.const) and (self.friend == other.friend) and (self.attrs == other.attrs)

    def __hash__(self) -> int:
        return hash((self.storage, self.threadLocal, self.inline, self.virtual, self.explicitSpec, self.consteval, self.constexpr, self.constinit, self.volatile, self.const, self.friend, self.attrs))

class ASTDeclSpecs(ASTBase):

    def __init__(self, outer: str, leftSpecs: ASTDeclSpecsSimple, rightSpecs: ASTDeclSpecsSimple, trailing: ASTTrailingTypeSpec) -> None:
        self.outer = outer
        self.leftSpecs = leftSpecs
        self.rightSpecs = rightSpecs
        self.allSpecs = self.leftSpecs.mergeWith(self.rightSpecs)
        self.trailingTypeSpec = trailing

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclSpecs):
            return NotImplemented
        return self.outer == other.outer and self.leftSpecs == other.leftSpecs and (self.rightSpecs == other.rightSpecs) and (self.trailingTypeSpec == other.trailingTypeSpec)

    def __hash__(self) -> int:
        return hash((self.outer, self.leftSpecs, self.rightSpecs, self.trailingTypeSpec))

class ASTArray(ASTBase):

    def __init__(self, size: ASTExpression) -> None:
        self.size = size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTArray):
            return NotImplemented
        return self.size == other.size

    def __hash__(self) -> int:
        return hash(self.size)

class ASTDeclarator(ASTBase):
    pass

class ASTDeclaratorNameParamQual(ASTDeclarator):

    def __init__(self, declId: ASTNestedName, arrayOps: list[ASTArray], paramQual: ASTParametersQualifiers) -> None:
        self.declId = declId
        self.arrayOps = arrayOps
        self.paramQual = paramQual

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclaratorNameParamQual):
            return NotImplemented
        return self.declId == other.declId and self.arrayOps == other.arrayOps and (self.paramQual == other.paramQual)

    def __hash__(self) -> int:
        return hash((self.declId, self.arrayOps, self.paramQual))

class ASTDeclaratorNameBitField(ASTDeclarator):

    def __init__(self, declId: ASTNestedName, size: ASTExpression) -> None:
        self.declId = declId
        self.size = size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclaratorNameBitField):
            return NotImplemented
        return self.declId == other.declId and self.size == other.size

    def __hash__(self) -> int:
        return hash((self.declId, self.size))

class ASTDeclaratorPtr(ASTDeclarator):

    def __init__(self, next: ASTDeclarator, volatile: bool, const: bool, attrs: ASTAttributeList) -> None:
        assert next
        self.next = next
        self.volatile = volatile
        self.const = const
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclaratorPtr):
            return NotImplemented
        return self.next == other.next and self.volatile == other.volatile and (self.const == other.const) and (self.attrs == other.attrs)

    def __hash__(self) -> int:
        return hash((self.next, self.volatile, self.const, self.attrs))

class ASTDeclaratorRef(ASTDeclarator):

    def __init__(self, next: ASTDeclarator, attrs: ASTAttributeList) -> None:
        assert next
        self.next = next
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclaratorRef):
            return NotImplemented
        return self.next == other.next and self.attrs == other.attrs

    def __hash__(self) -> int:
        return hash((self.next, self.attrs))

class ASTDeclaratorParamPack(ASTDeclarator):

    def __init__(self, next: ASTDeclarator) -> None:
        assert next
        self.next = next

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclaratorParamPack):
            return NotImplemented
        return self.next == other.next

    def __hash__(self) -> int:
        return hash(self.next)

class ASTDeclaratorMemPtr(ASTDeclarator):

    def __init__(self, className: ASTNestedName, const: bool, volatile: bool, next: ASTDeclarator) -> None:
        assert className
        assert next
        self.className = className
        self.const = const
        self.volatile = volatile
        self.next = next

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclaratorMemPtr):
            return NotImplemented
        return self.className == other.className and self.const == other.const and (self.volatile == other.volatile) and (self.next == other.next)

    def __hash__(self) -> int:
        return hash((self.className, self.const, self.volatile, self.next))

class ASTDeclaratorParen(ASTDeclarator):

    def __init__(self, inner: ASTDeclarator, next: ASTDeclarator) -> None:
        assert inner
        assert next
        self.inner = inner
        self.next = next

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclaratorParen):
            return NotImplemented
        return self.inner == other.inner and self.next == other.next

    def __hash__(self) -> int:
        return hash((self.inner, self.next))

class ASTPackExpansionExpr(ASTExpression):

    def __init__(self, expr: ASTExpression | ASTBracedInitList) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTPackExpansionExpr):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTParenExprList(ASTBaseParenExprList):

    def __init__(self, exprs: list[ASTExpression | ASTBracedInitList]) -> None:
        self.exprs = exprs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTParenExprList):
            return NotImplemented
        return self.exprs == other.exprs

    def __hash__(self) -> int:
        return hash(self.exprs)

class ASTInitializer(ASTBase):

    def __init__(self, value: ASTExpression | ASTBracedInitList, hasAssign: bool=True) -> None:
        self.value = value
        self.hasAssign = hasAssign

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTInitializer):
            return NotImplemented
        return self.value == other.value and self.hasAssign == other.hasAssign

    def __hash__(self) -> int:
        return hash((self.value, self.hasAssign))

class ASTType(ASTBase):

    def __init__(self, declSpecs: ASTDeclSpecs, decl: ASTDeclarator) -> None:
        assert declSpecs
        assert decl
        self.declSpecs = declSpecs
        self.decl = decl

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTType):
            return NotImplemented
        return self.declSpecs == other.declSpecs and self.decl == other.decl

    def __hash__(self) -> int:
        return hash((self.declSpecs, self.decl))

class ASTTemplateParamConstrainedTypeWithInit(ASTBase):

    def __init__(self, type: ASTType, init: ASTType) -> None:
        assert type
        self.type = type
        self.init = init

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTemplateParamConstrainedTypeWithInit):
            return NotImplemented
        return self.type == other.type and self.init == other.init

    def __hash__(self) -> int:
        return hash((self.type, self.init))

class ASTTypeWithInit(ASTBase):

    def __init__(self, type: ASTType, init: ASTInitializer) -> None:
        self.type = type
        self.init = init

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTypeWithInit):
            return NotImplemented
        return self.type == other.type and self.init == other.init

    def __hash__(self) -> int:
        return hash((self.type, self.init))

class ASTTypeUsing(ASTBase):

    def __init__(self, name: ASTNestedName, type: ASTType | None) -> None:
        self.name = name
        self.type = type

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTypeUsing):
            return NotImplemented
        return self.name == other.name and self.type == other.type

    def __hash__(self) -> int:
        return hash((self.name, self.type))

class ASTConcept(ASTBase):

    def __init__(self, nestedName: ASTNestedName, initializer: ASTInitializer) -> None:
        self.nestedName = nestedName
        self.initializer = initializer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTConcept):
            return NotImplemented
        return self.nestedName == other.nestedName and self.initializer == other.initializer

    def __hash__(self) -> int:
        return hash((self.nestedName, self.initializer))

class ASTBaseClass(ASTBase):

    def __init__(self, name: ASTNestedName, visibility: str, virtual: bool, pack: bool) -> None:
        self.name = name
        self.visibility = visibility
        self.virtual = virtual
        self.pack = pack

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTBaseClass):
            return NotImplemented
        return self.name == other.name and self.visibility == other.visibility and (self.virtual == other.virtual) and (self.pack == other.pack)

    def __hash__(self) -> int:
        return hash((self.name, self.visibility, self.virtual, self.pack))

class ASTClass(ASTBase):

    def __init__(self, name: ASTNestedName, final: bool, bases: list[ASTBaseClass], attrs: ASTAttributeList) -> None:
        self.name = name
        self.final = final
        self.bases = bases
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTClass):
            return NotImplemented
        return self.name == other.name and self.final == other.final and (self.bases == other.bases) and (self.attrs == other.attrs)

    def __hash__(self) -> int:
        return hash((self.name, self.final, self.bases, self.attrs))

class ASTUnion(ASTBase):

    def __init__(self, name: ASTNestedName, attrs: ASTAttributeList) -> None:
        self.name = name
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTUnion):
            return NotImplemented
        return self.name == other.name and self.attrs == other.attrs

    def __hash__(self) -> int:
        return hash((self.name, self.attrs))

class ASTEnum(ASTBase):

    def __init__(self, name: ASTNestedName, scoped: str, underlyingType: ASTType, attrs: ASTAttributeList) -> None:
        self.name = name
        self.scoped = scoped
        self.underlyingType = underlyingType
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTEnum):
            return NotImplemented
        return self.name == other.name and self.scoped == other.scoped and (self.underlyingType == other.underlyingType) and (self.attrs == other.attrs)

    def __hash__(self) -> int:
        return hash((self.name, self.scoped, self.underlyingType, self.attrs))

class ASTEnumerator(ASTBase):

    def __init__(self, name: ASTNestedName, init: ASTInitializer | None, attrs: ASTAttributeList) -> None:
        self.name = name
        self.init = init
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTEnumerator):
            return NotImplemented
        return self.name == other.name and self.init == other.init and (self.attrs == other.attrs)

    def __hash__(self) -> int:
        return hash((self.name, self.init, self.attrs))

class ASTTemplateParam(ASTBase):
    pass

class ASTTemplateKeyParamPackIdDefault(ASTTemplateParam):

    def __init__(self, key: str, identifier: ASTIdentifier, parameterPack: bool, default: ASTType) -> None:
        assert key
        if parameterPack:
            assert default is None
        self.key = key
        self.identifier = identifier
        self.parameterPack = parameterPack
        self.default = default

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTemplateKeyParamPackIdDefault):
            return NotImplemented
        return self.key == other.key and self.identifier == other.identifier and (self.parameterPack == other.parameterPack) and (self.default == other.default)

    def __hash__(self) -> int:
        return hash((self.key, self.identifier, self.parameterPack, self.default))

class ASTTemplateParamType(ASTTemplateParam):

    def __init__(self, data: ASTTemplateKeyParamPackIdDefault) -> None:
        assert data
        self.data = data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTemplateParamType):
            return NotImplemented
        return self.data == other.data

    def __hash__(self) -> int:
        return hash(self.data)

class ASTTemplateParamTemplateType(ASTTemplateParam):

    def __init__(self, nestedParams: ASTTemplateParams, data: ASTTemplateKeyParamPackIdDefault) -> None:
        assert nestedParams
        assert data
        self.nestedParams = nestedParams
        self.data = data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTemplateParamTemplateType):
            return NotImplemented
        return self.nestedParams == other.nestedParams and self.data == other.data

    def __hash__(self) -> int:
        return hash((self.nestedParams, self.data))

class ASTTemplateParamNonType(ASTTemplateParam):

    def __init__(self, param: ASTTypeWithInit | ASTTemplateParamConstrainedTypeWithInit, parameterPack: bool=False) -> None:
        assert param
        self.param = param
        self.parameterPack = parameterPack

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTemplateParamNonType):
            return NotImplemented
        return self.param == other.param and self.parameterPack == other.parameterPack

class ASTTemplateParams(ASTBase):

    def __init__(self, params: list[ASTTemplateParam], requiresClause: ASTRequiresClause | None) -> None:
        assert params is not None
        self.params = params
        self.requiresClause = requiresClause

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTemplateParams):
            return NotImplemented
        return self.params == other.params and self.requiresClause == other.requiresClause

    def __hash__(self) -> int:
        return hash((self.params, self.requiresClause))

class ASTTemplateIntroductionParameter(ASTBase):

    def __init__(self, identifier: ASTIdentifier, parameterPack: bool) -> None:
        self.identifier = identifier
        self.parameterPack = parameterPack

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTemplateIntroductionParameter):
            return NotImplemented
        return self.identifier == other.identifier and self.parameterPack == other.parameterPack

    def __hash__(self) -> int:
        return hash((self.identifier, self.parameterPack))

class ASTTemplateIntroduction(ASTBase):

    def __init__(self, concept: ASTNestedName, params: list[ASTTemplateIntroductionParameter]) -> None:
        assert len(params) > 0
        self.concept = concept
        self.params = params

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTemplateIntroduction):
            return NotImplemented
        return self.concept == other.concept and self.params == other.params

    def __hash__(self) -> int:
        return hash((self.concept, self.params))

class ASTTemplateDeclarationPrefix(ASTBase):

    def __init__(self, templates: list[ASTTemplateParams | ASTTemplateIntroduction] | None) -> None:
        self.templates = templates

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTemplateDeclarationPrefix):
            return NotImplemented
        return self.templates == other.templates

    def __hash__(self) -> int:
        return hash(self.templates)

class ASTRequiresClause(ASTBase):

    def __init__(self, expr: ASTExpression) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTRequiresClause):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTDeclaration(ASTBase):

    def __init__(self, objectType: str, directiveType: str | None=None, visibility: str | None=None, templatePrefix: ASTTemplateDeclarationPrefix | None=None, declaration: Any=None, trailingRequiresClause: ASTRequiresClause | None=None, semicolon: bool=False) -> None:
        self.objectType = objectType
        self.directiveType = directiveType
        self.visibility = visibility
        self.templatePrefix = templatePrefix
        self.declaration = declaration
        self.trailingRequiresClause = trailingRequiresClause
        self.semicolon = semicolon
        self.symbol: Symbol | None = None
        self.enumeratorScopedSymbol: Symbol | None = None
        self._newest_id_cache: str | None = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclaration):
            return NotImplemented
        return self.objectType == other.objectType and self.directiveType == other.directiveType and (self.visibility == other.visibility) and (self.templatePrefix == other.templatePrefix) and (self.declaration == other.declaration) and (self.trailingRequiresClause == other.trailingRequiresClause) and (self.semicolon == other.semicolon) and (self.symbol == other.symbol) and (self.enumeratorScopedSymbol == other.enumeratorScopedSymbol)

class ASTNamespace(ASTBase):

    def __init__(self, nestedName: ASTNestedName, templatePrefix: ASTTemplateDeclarationPrefix) -> None:
        self.nestedName = nestedName
        self.templatePrefix = templatePrefix

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTNamespace):
            return NotImplemented
        return self.nestedName == other.nestedName and self.templatePrefix == other.templatePrefix