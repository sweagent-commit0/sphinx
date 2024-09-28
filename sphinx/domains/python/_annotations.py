from __future__ import annotations
import ast
import functools
import operator
import token
from collections import deque
from inspect import Parameter
from typing import TYPE_CHECKING, Any
from docutils import nodes
from sphinx import addnodes
from sphinx.addnodes import desc_signature, pending_xref, pending_xref_condition
from sphinx.pycode.parser import Token, TokenProcessor
from sphinx.util.inspect import signature_from_str
if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from docutils.nodes import Element, Node
    from sphinx.environment import BuildEnvironment

def parse_reftarget(reftarget: str, suppress_prefix: bool=False) -> tuple[str, str, str, bool]:
    """Parse a type string and return (reftype, reftarget, title, refspecific flag)"""
    pass

def type_to_xref(target: str, env: BuildEnvironment, *, suppress_prefix: bool=False) -> addnodes.pending_xref:
    """Convert a type string to a cross reference node."""
    pass

def _parse_annotation(annotation: str, env: BuildEnvironment) -> list[Node]:
    """Parse type annotation."""
    pass

class _TypeParameterListParser(TokenProcessor):

    def __init__(self, sig: str) -> None:
        signature = sig.replace('\n', '').strip()
        super().__init__([signature])
        self.type_params: list[tuple[str, int, Any, Any]] = []

def _parse_type_list(tp_list: str, env: BuildEnvironment, multi_line_parameter_list: bool=False) -> addnodes.desc_type_parameter_list:
    """Parse a list of type parameters according to PEP 695."""
    pass

def _parse_arglist(arglist: str, env: BuildEnvironment, multi_line_parameter_list: bool=False) -> addnodes.desc_parameterlist:
    """Parse a list of arguments using AST parser"""
    pass

def _pseudo_parse_arglist(signode: desc_signature, arglist: str, multi_line_parameter_list: bool=False) -> None:
    """"Parse" a list of arguments separated by commas.

    Arguments can have "optional" annotations given by enclosing them in
    brackets.  Currently, this will split at any comma, even if it's inside a
    string literal (e.g. default argument value).
    """
    pass