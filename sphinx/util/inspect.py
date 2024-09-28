"""Helpers for inspecting Python modules."""
from __future__ import annotations
import ast
import builtins
import contextlib
import enum
import inspect
import re
import sys
import types
import typing
from collections.abc import Mapping
from functools import cached_property, partial, partialmethod, singledispatchmethod
from importlib import import_module
from inspect import Parameter, Signature
from io import StringIO
from types import ClassMethodDescriptorType, MethodDescriptorType, WrapperDescriptorType
from typing import TYPE_CHECKING, Any, ForwardRef
from sphinx.pycode.ast import unparse as ast_unparse
from sphinx.util import logging
from sphinx.util.typing import stringify_annotation
if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from inspect import _ParameterKind
    from types import MethodType, ModuleType
    from typing import Final, Protocol, TypeAlias
    from typing_extensions import TypeIs

    class _SupportsGet(Protocol):

        def __get__(self, __instance: Any, __owner: type | None=...) -> Any:
            ...

    class _SupportsSet(Protocol):

        def __set__(self, __instance: Any, __value: Any) -> None:
            ...

    class _SupportsDelete(Protocol):

        def __delete__(self, __instance: Any) -> None:
            ...
    _RoutineType: TypeAlias = types.FunctionType | types.LambdaType | types.MethodType | types.BuiltinFunctionType | types.BuiltinMethodType | types.WrapperDescriptorType | types.MethodDescriptorType | types.ClassMethodDescriptorType
    _SignatureType: TypeAlias = Callable[..., Any] | staticmethod | classmethod
logger = logging.getLogger(__name__)
memory_address_re = re.compile(' at 0x[0-9a-f]{8,16}(?=>)', re.IGNORECASE)
isasyncgenfunction = inspect.isasyncgenfunction
ismethod = inspect.ismethod
ismethoddescriptor = inspect.ismethoddescriptor
isclass = inspect.isclass
ismodule = inspect.ismodule

def unwrap(obj: Any) -> Any:
    """Get an original object from wrapped object (wrapped functions).

    Mocked objects are returned as is.
    """
    pass

def unwrap_all(obj: Any, *, stop: Callable[[Any], bool] | None=None) -> Any:
    """Get an original object from wrapped object.

    Unlike :func:`unwrap`, this unwraps partial functions, wrapped functions,
    class methods and static methods.

    When specified, *stop* is a predicate indicating whether an object should
    be unwrapped or not.
    """
    pass

def getall(obj: Any) -> Sequence[str] | None:
    """Get the ``__all__`` attribute of an object as a sequence.

    This returns ``None`` if the given ``obj.__all__`` does not exist and
    raises :exc:`ValueError` if ``obj.__all__`` is not a list or tuple of
    strings.
    """
    pass

def getannotations(obj: Any) -> Mapping[str, Any]:
    """Safely get the ``__annotations__`` attribute of an object."""
    pass

def getglobals(obj: Any) -> Mapping[str, Any]:
    """Safely get :attr:`obj.__globals__ <function.__globals__>`."""
    pass

def getmro(obj: Any) -> tuple[type, ...]:
    """Safely get :attr:`obj.__mro__ <class.__mro__>`."""
    pass

def getorigbases(obj: Any) -> tuple[Any, ...] | None:
    """Safely get ``obj.__orig_bases__``.

    This returns ``None`` if the object is not a class or if ``__orig_bases__``
    is not well-defined (e.g., a non-tuple object or an empty sequence).
    """
    pass

def getslots(obj: Any) -> dict[str, Any] | dict[str, None] | None:
    """Safely get :term:`obj.__slots__ <__slots__>` as a dictionary if any.

    - This returns ``None`` if ``obj.__slots__`` does not exist.
    - This raises a :exc:`TypeError` if *obj* is not a class.
    - This raises a :exc:`ValueError` if ``obj.__slots__`` is invalid.
    """
    pass

def isenumclass(x: Any) -> TypeIs[type[enum.Enum]]:
    """Check if the object is an :class:`enumeration class <enum.Enum>`."""
    pass

def isenumattribute(x: Any) -> TypeIs[enum.Enum]:
    """Check if the object is an enumeration attribute."""
    pass

def unpartial(obj: Any) -> Any:
    """Get an original object from a partial-like object.

    If *obj* is not a partial object, it is returned as is.

    .. seealso:: :func:`ispartial`
    """
    pass

def ispartial(obj: Any) -> TypeIs[partial | partialmethod]:
    """Check if the object is a partial function or method."""
    pass

def isclassmethod(obj: Any, cls: Any=None, name: str | None=None) -> TypeIs[classmethod]:
    """Check if the object is a :class:`classmethod`."""
    pass

def isstaticmethod(obj: Any, cls: Any=None, name: str | None=None) -> TypeIs[staticmethod]:
    """Check if the object is a :class:`staticmethod`."""
    pass

def isdescriptor(x: Any) -> TypeIs[_SupportsGet | _SupportsSet | _SupportsDelete]:
    """Check if the object is a :external+python:term:`descriptor`."""
    pass

def isabstractmethod(obj: Any) -> bool:
    """Check if the object is an :func:`abstractmethod`."""
    pass

def isboundmethod(method: MethodType) -> bool:
    """Check if the method is a bound method."""
    pass

def is_cython_function_or_method(obj: Any) -> bool:
    """Check if the object is a function or method in cython."""
    pass
_DESCRIPTOR_LIKE: Final[tuple[type, ...]] = (ClassMethodDescriptorType, MethodDescriptorType, WrapperDescriptorType)

def isattributedescriptor(obj: Any) -> bool:
    """Check if the object is an attribute-like descriptor."""
    pass

def is_singledispatch_function(obj: Any) -> bool:
    """Check if the object is a :func:`~functools.singledispatch` function."""
    pass

def is_singledispatch_method(obj: Any) -> TypeIs[singledispatchmethod]:
    """Check if the object is a :class:`~functools.singledispatchmethod`."""
    pass

def isfunction(obj: Any) -> TypeIs[types.FunctionType]:
    """Check if the object is a user-defined function.

    Partial objects are unwrapped before checking them.

    .. seealso:: :external+python:func:`inspect.isfunction`
    """
    pass

def isbuiltin(obj: Any) -> TypeIs[types.BuiltinFunctionType]:
    """Check if the object is a built-in function or method.

    Partial objects are unwrapped before checking them.

    .. seealso:: :external+python:func:`inspect.isbuiltin`
    """
    pass

def isroutine(obj: Any) -> TypeIs[_RoutineType]:
    """Check if the object is a kind of function or method.

    Partial objects are unwrapped before checking them.

    .. seealso:: :external+python:func:`inspect.isroutine`
    """
    pass

def iscoroutinefunction(obj: Any) -> TypeIs[Callable[..., types.CoroutineType]]:
    """Check if the object is a :external+python:term:`coroutine` function."""
    pass

def _is_wrapped_coroutine(obj: Any) -> bool:
    """Check if the object is wrapped coroutine-function."""
    pass

def isproperty(obj: Any) -> TypeIs[property | cached_property]:
    """Check if the object is property (possibly cached)."""
    pass

def isgenericalias(obj: Any) -> TypeIs[types.GenericAlias]:
    """Check if the object is a generic alias."""
    pass

def safe_getattr(obj: Any, name: str, *defargs: Any) -> Any:
    """A getattr() that turns all exceptions into AttributeErrors."""
    pass

def object_description(obj: Any, *, _seen: frozenset[int]=frozenset()) -> str:
    """A repr() implementation that returns text safe to use in reST context.

    Maintains a set of 'seen' object IDs to detect and avoid infinite recursion.
    """
    pass

def is_builtin_class_method(obj: Any, attr_name: str) -> bool:
    """Check whether *attr_name* is implemented on a builtin class.

        >>> is_builtin_class_method(int, '__init__')
        True


    This function is needed since CPython implements ``int.__init__`` via
    descriptors, but PyPy implementation is written in pure Python code.
    """
    pass

class DefaultValue:
    """A simple wrapper for default value of the parameters of overload functions."""

    def __init__(self, value: str) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        return self.value == other

    def __repr__(self) -> str:
        return self.value

class TypeAliasForwardRef:
    """Pseudo typing class for :confval:`autodoc_type_aliases`.

    This avoids the error on evaluating the type inside :func:`typing.get_type_hints()`.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        return self.name == other

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return self.name

class TypeAliasModule:
    """Pseudo module class for :confval:`autodoc_type_aliases`."""

    def __init__(self, modname: str, mapping: Mapping[str, str]) -> None:
        self.__modname = modname
        self.__mapping = mapping
        self.__module: ModuleType | None = None

    def __getattr__(self, name: str) -> Any:
        fullname = '.'.join(filter(None, [self.__modname, name]))
        if fullname in self.__mapping:
            return TypeAliasForwardRef(self.__mapping[fullname])
        else:
            prefix = fullname + '.'
            nested = {k: v for k, v in self.__mapping.items() if k.startswith(prefix)}
            if nested:
                return TypeAliasModule(fullname, nested)
            else:
                try:
                    return import_module(fullname)
                except ImportError:
                    if self.__module is None:
                        self.__module = import_module(self.__modname)
                    return getattr(self.__module, name)

class TypeAliasNamespace(dict[str, Any]):
    """Pseudo namespace class for :confval:`autodoc_type_aliases`.

    Useful for looking up nested objects via ``namespace.foo.bar.Class``.
    """

    def __init__(self, mapping: Mapping[str, str]) -> None:
        super().__init__()
        self.__mapping = mapping

    def __getitem__(self, key: str) -> Any:
        if key in self.__mapping:
            return TypeAliasForwardRef(self.__mapping[key])
        else:
            prefix = key + '.'
            nested = {k: v for k, v in self.__mapping.items() if k.startswith(prefix)}
            if nested:
                return TypeAliasModule(key, nested)
            else:
                raise KeyError

def _should_unwrap(subject: _SignatureType) -> bool:
    """Check the function should be unwrapped on getting signature."""
    pass

def signature(subject: _SignatureType, bound_method: bool=False, type_aliases: Mapping[str, str] | None=None) -> Signature:
    """Return a Signature object for the given *subject*.

    :param bound_method: Specify *subject* is a bound method or not
    """
    pass

def evaluate_signature(sig: Signature, globalns: dict[str, Any] | None=None, localns: dict[str, Any] | None=None) -> Signature:
    """Evaluate unresolved type annotations in a signature object."""
    pass

def _evaluate_forwardref(ref: ForwardRef, globalns: dict[str, Any] | None, localns: dict[str, Any] | None) -> Any:
    """Evaluate a forward reference."""
    pass

def _evaluate(annotation: Any, globalns: dict[str, Any], localns: dict[str, Any]) -> Any:
    """Evaluate unresolved type annotation."""
    pass

def stringify_signature(sig: Signature, show_annotation: bool=True, show_return_annotation: bool=True, unqualified_typehints: bool=False) -> str:
    """Stringify a :class:`~inspect.Signature` object.

    :param show_annotation: If enabled, show annotations on the signature
    :param show_return_annotation: If enabled, show annotation of the return value
    :param unqualified_typehints: If enabled, show annotations as unqualified
                                  (ex. io.StringIO -> StringIO)
    """
    pass

def signature_from_str(signature: str) -> Signature:
    """Create a :class:`~inspect.Signature` object from a string."""
    pass

def signature_from_ast(node: ast.FunctionDef, code: str='') -> Signature:
    """Create a :class:`~inspect.Signature` object from an AST node."""
    pass

def getdoc(obj: Any, attrgetter: Callable=safe_getattr, allow_inherited: bool=False, cls: Any=None, name: str | None=None) -> str | None:
    """Get the docstring for the object.

    This tries to obtain the docstring for some kind of objects additionally:

    * partial functions
    * inherited docstring
    * inherited decorated methods
    """
    pass