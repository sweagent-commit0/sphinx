"""Generating content for autodoc using typehints"""
from __future__ import annotations
import re
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, cast
from docutils import nodes
import sphinx
from sphinx import addnodes
from sphinx.util import inspect
from sphinx.util.typing import ExtensionMetadata, stringify_annotation
if TYPE_CHECKING:
    from docutils.nodes import Element
    from sphinx.application import Sphinx
    from sphinx.ext.autodoc import Options

def record_typehints(app: Sphinx, objtype: str, name: str, obj: Any, options: Options, args: str, retann: str) -> None:
    """Record type hints to env object."""
    pass