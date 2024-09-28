"""Provides the ``ifconfig`` directive.

The ``ifconfig`` directive enables writing documentation
that is included depending on configuration variables.

Usage::

    .. ifconfig:: releaselevel in ('alpha', 'beta', 'rc')

       This stuff is only included in the built docs for unstable versions.

The argument for ``ifconfig`` is a plain Python expression, evaluated in the
namespace of the project configuration (that is, all variables from
``conf.py`` are available.)
"""
from __future__ import annotations
from typing import TYPE_CHECKING, ClassVar
from docutils import nodes
import sphinx
from sphinx.util.docutils import SphinxDirective
if TYPE_CHECKING:
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata, OptionSpec

class ifconfig(nodes.Element):
    pass

class IfConfig(SphinxDirective):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[OptionSpec] = {}