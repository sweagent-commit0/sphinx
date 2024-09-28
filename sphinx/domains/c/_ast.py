from __future__ import annotations
import sys
import warnings
from typing import TYPE_CHECKING, Any, Union, cast
from docutils import nodes
from sphinx import addnodes
from sphinx.domains.c._ids import _id_prefix, _max_id
from sphinx.util.cfamily import ASTAttributeList, ASTBaseBase, ASTBaseParenExprList, UnsupportedMultiCharacterCharLiteral, verify_description_mode
if TYPE_CHECKING:
    from typing import TypeAlias
    from docutils.nodes import Element, Node, TextElement
    from sphinx.domains.c._symbol import Symbol
    from sphinx.environment import BuildEnvironment
    from sphinx.util.cfamily import StringifyTransform
DeclarationType: TypeAlias = Union['ASTStruct', 'ASTUnion', 'ASTEnum', 'ASTEnumerator', 'ASTType', 'ASTTypeWithInit', 'ASTMacro']

class ASTBase(ASTBaseBase):
    pass

class ASTIdentifier(ASTBaseBase):

    def __init__(self, name: str) -> None:
        if not isinstance(name, str) or len(name) == 0:
            raise AssertionError
        self.name = sys.intern(name)
        self.is_anonymous = name[0] == '@'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTIdentifier):
            return NotImplemented
        return self.name == other.name

    def __str__(self) -> str:
        return self.name

class ASTNestedName(ASTBase):

    def __init__(self, names: list[ASTIdentifier], rooted: bool) -> None:
        assert len(names) > 0
        self.names = names
        self.rooted = rooted

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTNestedName):
            return NotImplemented
        return self.names == other.names and self.rooted == other.rooted

    def __hash__(self) -> int:
        return hash((self.names, self.rooted))

class ASTExpression(ASTBase):
    pass

class ASTLiteral(ASTExpression):
    pass

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

class ASTCharLiteral(ASTLiteral):

    def __init__(self, prefix: str, data: str) -> None:
        self.prefix = prefix
        self.data = data
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

class ASTStringLiteral(ASTLiteral):

    def __init__(self, data: str) -> None:
        self.data = data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTStringLiteral):
            return NotImplemented
        return self.data == other.data

    def __hash__(self) -> int:
        return hash(self.data)

class ASTIdExpression(ASTExpression):

    def __init__(self, name: ASTNestedName) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTIdExpression):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

class ASTParenExpr(ASTExpression):

    def __init__(self, expr: ASTExpression) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTParenExpr):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTPostfixOp(ASTBase):
    pass

class ASTPostfixCallExpr(ASTPostfixOp):

    def __init__(self, lst: ASTParenExprList | ASTBracedInitList) -> None:
        self.lst = lst

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTPostfixCallExpr):
            return NotImplemented
        return self.lst == other.lst

    def __hash__(self) -> int:
        return hash(self.lst)

class ASTPostfixArray(ASTPostfixOp):

    def __init__(self, expr: ASTExpression) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTPostfixArray):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTPostfixInc(ASTPostfixOp):
    pass

class ASTPostfixDec(ASTPostfixOp):
    pass

class ASTPostfixMemberOfPointer(ASTPostfixOp):

    def __init__(self, name: ASTNestedName) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTPostfixMemberOfPointer):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

class ASTPostfixExpr(ASTExpression):

    def __init__(self, prefix: ASTExpression, postFixes: list[ASTPostfixOp]) -> None:
        self.prefix = prefix
        self.postFixes = postFixes

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTPostfixExpr):
            return NotImplemented
        return self.prefix == other.prefix and self.postFixes == other.postFixes

    def __hash__(self) -> int:
        return hash((self.prefix, self.postFixes))

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

class ASTBinOpExpr(ASTBase):

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

class ASTAssignmentExpr(ASTExpression):

    def __init__(self, exprs: list[ASTExpression], ops: list[str]) -> None:
        assert len(exprs) > 0
        assert len(exprs) == len(ops) + 1
        self.exprs = exprs
        self.ops = ops

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTAssignmentExpr):
            return NotImplemented
        return self.exprs == other.exprs and self.ops == other.ops

    def __hash__(self) -> int:
        return hash((self.exprs, self.ops))

class ASTFallbackExpr(ASTExpression):

    def __init__(self, expr: str) -> None:
        self.expr = expr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTFallbackExpr):
            return NotImplemented
        return self.expr == other.expr

    def __hash__(self) -> int:
        return hash(self.expr)

class ASTTrailingTypeSpec(ASTBase):
    pass

class ASTTrailingTypeSpecFundamental(ASTTrailingTypeSpec):

    def __init__(self, names: list[str]) -> None:
        assert len(names) != 0
        self.names = names

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTrailingTypeSpecFundamental):
            return NotImplemented
        return self.names == other.names

    def __hash__(self) -> int:
        return hash(self.names)

class ASTTrailingTypeSpecName(ASTTrailingTypeSpec):

    def __init__(self, prefix: str, nestedName: ASTNestedName) -> None:
        self.prefix = prefix
        self.nestedName = nestedName

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTTrailingTypeSpecName):
            return NotImplemented
        return self.prefix == other.prefix and self.nestedName == other.nestedName

    def __hash__(self) -> int:
        return hash((self.prefix, self.nestedName))

class ASTFunctionParameter(ASTBase):

    def __init__(self, arg: ASTTypeWithInit | None, ellipsis: bool=False) -> None:
        self.arg = arg
        self.ellipsis = ellipsis

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTFunctionParameter):
            return NotImplemented
        return self.arg == other.arg and self.ellipsis == other.ellipsis

    def __hash__(self) -> int:
        return hash((self.arg, self.ellipsis))

class ASTParameters(ASTBase):

    def __init__(self, args: list[ASTFunctionParameter], attrs: ASTAttributeList) -> None:
        self.args = args
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTParameters):
            return NotImplemented
        return self.args == other.args and self.attrs == other.attrs

    def __hash__(self) -> int:
        return hash((self.args, self.attrs))

class ASTDeclSpecsSimple(ASTBaseBase):

    def __init__(self, storage: str, threadLocal: str, inline: bool, restrict: bool, volatile: bool, const: bool, attrs: ASTAttributeList) -> None:
        self.storage = storage
        self.threadLocal = threadLocal
        self.inline = inline
        self.restrict = restrict
        self.volatile = volatile
        self.const = const
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclSpecsSimple):
            return NotImplemented
        return self.storage == other.storage and self.threadLocal == other.threadLocal and (self.inline == other.inline) and (self.restrict == other.restrict) and (self.volatile == other.volatile) and (self.const == other.const) and (self.attrs == other.attrs)

    def __hash__(self) -> int:
        return hash((self.storage, self.threadLocal, self.inline, self.restrict, self.volatile, self.const, self.attrs))

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

    def __init__(self, static: bool, const: bool, volatile: bool, restrict: bool, vla: bool, size: ASTExpression) -> None:
        self.static = static
        self.const = const
        self.volatile = volatile
        self.restrict = restrict
        self.vla = vla
        self.size = size
        if vla:
            assert size is None
        if size is not None:
            assert not vla

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTArray):
            return NotImplemented
        return self.static == other.static and self.const == other.const and (self.volatile == other.volatile) and (self.restrict == other.restrict) and (self.vla == other.vla) and (self.size == other.size)

    def __hash__(self) -> int:
        return hash((self.static, self.const, self.volatile, self.restrict, self.vla, self.size))

class ASTDeclarator(ASTBase):
    pass

class ASTDeclaratorNameParam(ASTDeclarator):

    def __init__(self, declId: ASTNestedName, arrayOps: list[ASTArray], param: ASTParameters) -> None:
        self.declId = declId
        self.arrayOps = arrayOps
        self.param = param

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclaratorNameParam):
            return NotImplemented
        return self.declId == other.declId and self.arrayOps == other.arrayOps and (self.param == other.param)

    def __hash__(self) -> int:
        return hash((self.declId, self.arrayOps, self.param))

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

    def __init__(self, next: ASTDeclarator, restrict: bool, volatile: bool, const: bool, attrs: ASTAttributeList) -> None:
        assert next
        self.next = next
        self.restrict = restrict
        self.volatile = volatile
        self.const = const
        self.attrs = attrs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclaratorPtr):
            return NotImplemented
        return self.next == other.next and self.restrict == other.restrict and (self.volatile == other.volatile) and (self.const == other.const) and (self.attrs == other.attrs)

    def __hash__(self) -> int:
        return hash((self.next, self.restrict, self.volatile, self.const, self.attrs))

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

class ASTParenExprList(ASTBaseParenExprList):

    def __init__(self, exprs: list[ASTExpression]) -> None:
        self.exprs = exprs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTParenExprList):
            return NotImplemented
        return self.exprs == other.exprs

    def __hash__(self) -> int:
        return hash(self.exprs)

class ASTBracedInitList(ASTBase):

    def __init__(self, exprs: list[ASTExpression], trailingComma: bool) -> None:
        self.exprs = exprs
        self.trailingComma = trailingComma

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTBracedInitList):
            return NotImplemented
        return self.exprs == other.exprs and self.trailingComma == other.trailingComma

    def __hash__(self) -> int:
        return hash((self.exprs, self.trailingComma))

class ASTInitializer(ASTBase):

    def __init__(self, value: ASTBracedInitList | ASTExpression, hasAssign: bool=True) -> None:
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

class ASTMacroParameter(ASTBase):

    def __init__(self, arg: ASTNestedName | None, ellipsis: bool=False, variadic: bool=False) -> None:
        self.arg = arg
        self.ellipsis = ellipsis
        self.variadic = variadic

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTMacroParameter):
            return NotImplemented
        return self.arg == other.arg and self.ellipsis == other.ellipsis and (self.variadic == other.variadic)

    def __hash__(self) -> int:
        return hash((self.arg, self.ellipsis, self.variadic))

class ASTMacro(ASTBase):

    def __init__(self, ident: ASTNestedName, args: list[ASTMacroParameter] | None) -> None:
        self.ident = ident
        self.args = args

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTMacro):
            return NotImplemented
        return self.ident == other.ident and self.args == other.args

    def __hash__(self) -> int:
        return hash((self.ident, self.args))

class ASTStruct(ASTBase):

    def __init__(self, name: ASTNestedName) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTStruct):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

class ASTUnion(ASTBase):

    def __init__(self, name: ASTNestedName) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTUnion):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

class ASTEnum(ASTBase):

    def __init__(self, name: ASTNestedName) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTEnum):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

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

class ASTDeclaration(ASTBaseBase):

    def __init__(self, objectType: str, directiveType: str | None, declaration: DeclarationType | ASTFunctionParameter, semicolon: bool=False) -> None:
        self.objectType = objectType
        self.directiveType = directiveType
        self.declaration = declaration
        self.semicolon = semicolon
        self.symbol: Symbol | None = None
        self.enumeratorScopedSymbol: Symbol | None = None
        self._newest_id_cache: str | None = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTDeclaration):
            return NotImplemented
        return self.objectType == other.objectType and self.directiveType == other.directiveType and (self.declaration == other.declaration) and (self.semicolon == other.semicolon) and (self.symbol == other.symbol) and (self.enumeratorScopedSymbol == other.enumeratorScopedSymbol)