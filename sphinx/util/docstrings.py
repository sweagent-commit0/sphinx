"""Utilities for docstring processing."""
from __future__ import annotations
import re
import sys
from docutils.parsers.rst.states import Body
field_list_item_re = re.compile(Body.patterns['field_marker'])

def separate_metadata(s: str | None) -> tuple[str | None, dict[str, str]]:
    """Separate docstring into metadata and others."""
    pass

def prepare_docstring(s: str, tabsize: int=8) -> list[str]:
    """Convert a docstring into lines of parseable reST.  Remove common leading
    indentation, where the indentation of the first line is ignored.

    Return the docstring as a list of lines usable for inserting into a docutils
    ViewList (used as argument of nested_parse().)  An empty line is added to
    act as a separator between this docstring and following content.
    """
    pass

def prepare_commentdoc(s: str) -> list[str]:
    """Extract documentation comment lines (starting with #:) and return them
    as a list of lines.  Returns an empty list if there is no documentation.
    """
    pass