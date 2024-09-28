"""Importer utilities for autodoc"""
from __future__ import annotations
import contextlib
import importlib
import os
import sys
import traceback
import typing
from enum import Enum
from typing import TYPE_CHECKING, NamedTuple
from sphinx.errors import PycodeError
from sphinx.ext.autodoc.mock import ismock, undecorate
from sphinx.pycode import ModuleAnalyzer
from sphinx.util import logging
from sphinx.util.inspect import getannotations, getmro, getslots, isclass, isenumclass, safe_getattr, unwrap_all
if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Mapping
    from types import ModuleType
    from typing import Any
    from sphinx.ext.autodoc import ObjectMember
logger = logging.getLogger(__name__)

def _filter_enum_dict(enum_class: type[Enum], attrgetter: Callable[[Any, str, Any], Any], enum_class_dict: Mapping[str, object]) -> Iterator[tuple[str, type, Any]]:
    """Find the attributes to document of an enumeration class.

    The output consists of triplets ``(attribute name, defining class, value)``
    where the attribute name can appear more than once during the iteration
    but with different defining class. The order of occurrence is guided by
    the MRO of *enum_class*.
    """
    pass

def mangle(subject: Any, name: str) -> str:
    """Mangle the given name."""
    pass

def unmangle(subject: Any, name: str) -> str | None:
    """Unmangle the given name."""
    pass

def import_module(modname: str) -> Any:
    """Call importlib.import_module(modname), convert exceptions to ImportError."""
    pass

def _reload_module(module: ModuleType) -> Any:
    """
    Call importlib.reload(module), convert exceptions to ImportError
    """
    pass

class Attribute(NamedTuple):
    name: str
    directly_defined: bool
    value: Any

def get_object_members(subject: Any, objpath: list[str], attrgetter: Callable, analyzer: ModuleAnalyzer | None=None) -> dict[str, Attribute]:
    """Get members and attributes of target object."""
    pass

def get_class_members(subject: Any, objpath: Any, attrgetter: Callable, inherit_docstrings: bool=True) -> dict[str, ObjectMember]:
    """Get members and attributes of target class."""
    pass