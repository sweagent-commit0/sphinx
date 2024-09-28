from __future__ import annotations
import re
from os.path import abspath, relpath
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, cast
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.parsers.rst.directives.misc import Class
from docutils.parsers.rst.directives.misc import Include as BaseInclude
from docutils.statemachine import StateMachine
from sphinx import addnodes
from sphinx.domains.std import StandardDomain
from sphinx.locale import _, __
from sphinx.util import docname_join, logging, url_re
from sphinx.util.docutils import SphinxDirective
from sphinx.util.matching import Matcher, patfilter
from sphinx.util.nodes import explicit_title_re
if TYPE_CHECKING:
    from collections.abc import Sequence
    from docutils.nodes import Element, Node
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
glob_re = re.compile('.*[*?\\[].*')
logger = logging.getLogger(__name__)

class TocTree(SphinxDirective):
    """
    Directive to notify Sphinx about the hierarchical structure of the docs,
    and to include a table-of-contents like tree in the current document.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {'maxdepth': int, 'name': directives.unchanged, 'class': directives.class_option, 'caption': directives.unchanged_required, 'glob': directives.flag, 'hidden': directives.flag, 'includehidden': directives.flag, 'numbered': int_or_nothing, 'titlesonly': directives.flag, 'reversed': directives.flag}

    def parse_content(self, toctree: addnodes.toctree) -> None:
        """
        Populate ``toctree['entries']`` and ``toctree['includefiles']`` from content.
        """
        pass

class Author(SphinxDirective):
    """
    Directive to give the name of the author of the current document
    or section. Shown in the output only if the show_authors option is on.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[OptionSpec] = {}

class SeeAlso(BaseAdmonition):
    """
    An admonition mentioning things to look at as reference.
    """
    node_class = addnodes.seealso

class TabularColumns(SphinxDirective):
    """
    Directive to give an explicit tabulary column definition to LaTeX.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[OptionSpec] = {}

class Centered(SphinxDirective):
    """
    Directive to create a centered line of bold text.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[OptionSpec] = {}

class Acks(SphinxDirective):
    """
    Directive for a list of names.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec: ClassVar[OptionSpec] = {}

class HList(SphinxDirective):
    """
    Directive for a list that gets compacted horizontally.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec: ClassVar[OptionSpec] = {'columns': int}

class Only(SphinxDirective):
    """
    Directive to only include text if the given tag(s) are enabled.
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[OptionSpec] = {}

class Include(BaseInclude, SphinxDirective):
    """
    Like the standard "Include" directive, but interprets absolute paths
    "correctly", i.e. relative to source directory.
    """