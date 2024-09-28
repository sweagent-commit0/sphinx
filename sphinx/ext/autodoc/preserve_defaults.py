"""Preserve function defaults.

Preserve the default argument values of function signatures in source code
and keep them not evaluated for readability.
"""
from __future__ import annotations
import ast
import inspect
import types
import warnings
from typing import TYPE_CHECKING
import sphinx
from sphinx.deprecation import RemovedInSphinx90Warning
from sphinx.locale import __
from sphinx.pycode.ast import unparse as ast_unparse
from sphinx.util import logging
if TYPE_CHECKING:
    from typing import Any
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)
_LAMBDA_NAME = (lambda: None).__name__

class DefaultValue:

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

def get_function_def(obj: Any) -> ast.FunctionDef | None:
    """Get FunctionDef object from living object.

    This tries to parse original code for living object and returns
    AST node for given *obj*.
    """
    pass

def _get_arguments(obj: Any, /) -> ast.arguments | None:
    """Parse 'ast.arguments' from an object.

    This tries to parse the original code for an object and returns
    an 'ast.arguments' node.
    """
    pass

def update_defvalue(app: Sphinx, obj: Any, bound_method: bool) -> None:
    """Update defvalue info of *obj* using type_comments."""
    pass