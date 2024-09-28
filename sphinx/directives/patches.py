from __future__ import annotations
import os
from os import path
from typing import TYPE_CHECKING, ClassVar, cast
from docutils import nodes
from docutils.nodes import Node, make_id
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives import images, tables
from docutils.parsers.rst.directives.misc import Meta
from docutils.parsers.rst.roles import set_classes
from sphinx.directives import optional_int
from sphinx.domains.math import MathDomain
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import set_source_info
from sphinx.util.osutil import SEP, os_path, relpath
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
logger = logging.getLogger(__name__)

class Figure(images.Figure):
    """The figure directive which applies `:name:` option to the figure node
    instead of the image node.
    """

class CSVTable(tables.CSVTable):
    """The csv-table directive which searches a CSV file from Sphinx project's source
    directory when an absolute path is given via :file: option.
    """

class Code(SphinxDirective):
    """Parse and mark up content of a code block.

    This is compatible with docutils' :rst:dir:`code` directive.
    """
    optional_arguments = 1
    option_spec: ClassVar[OptionSpec] = {'class': directives.class_option, 'force': directives.flag, 'name': directives.unchanged, 'number-lines': optional_int}
    has_content = True

class MathDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec: ClassVar[OptionSpec] = {'label': directives.unchanged, 'name': directives.unchanged, 'class': directives.class_option, 'nowrap': directives.flag}

class Rubric(SphinxDirective):
    """A patch of the docutils' :rst:dir:`rubric` directive,
    which adds a level option to specify the heading level of the rubric.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'class': directives.class_option, 'name': directives.unchanged, 'heading-level': lambda c: directives.choice(c, ('1', '2', '3', '4', '5', '6'))}