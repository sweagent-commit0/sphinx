"""Update annotations info of living objects using type_comments."""
from __future__ import annotations
import ast
from inspect import Parameter, Signature, getsource
from typing import TYPE_CHECKING, Any, cast
import sphinx
from sphinx.locale import __
from sphinx.pycode.ast import unparse as ast_unparse
from sphinx.util import inspect, logging
if TYPE_CHECKING:
    from collections.abc import Sequence
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

def not_suppressed(argtypes: Sequence[ast.expr]=()) -> bool:
    """Check given *argtypes* is suppressed type_comment or not."""
    pass

def signature_from_ast(node: ast.FunctionDef, bound_method: bool, type_comment: ast.FunctionDef) -> Signature:
    """Return a Signature object for the given *node*.

    :param bound_method: Specify *node* is a bound method or not
    """
    pass

def get_type_comment(obj: Any, bound_method: bool=False) -> Signature | None:
    """Get type_comment'ed FunctionDef object from living object.

    This tries to parse original code for living object and returns
    Signature for given *obj*.
    """
    pass

def update_annotations_using_type_comments(app: Sphinx, obj: Any, bound_method: bool) -> None:
    """Update annotations info of *obj* using type_comments."""
    pass