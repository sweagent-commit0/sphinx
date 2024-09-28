"""Mimic doctest in Sphinx.

The extension automatically execute code snippets and checks their results.
"""
from __future__ import annotations
import doctest
import re
import sys
import time
from io import StringIO
from os import path
from typing import TYPE_CHECKING, Any, ClassVar
from docutils import nodes
from docutils.parsers.rst import directives
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import Version
import sphinx
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.console import bold
from sphinx.util.docutils import SphinxDirective
from sphinx.util.osutil import relpath
if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Sequence
    from docutils.nodes import Element, Node, TextElement
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
logger = logging.getLogger(__name__)
blankline_re = re.compile('^\\s*<BLANKLINE>', re.MULTILINE)
doctestopt_re = re.compile('#\\s*doctest:.+$', re.MULTILINE)

def is_allowed_version(spec: str, version: str) -> bool:
    """Check `spec` satisfies `version` or not.

    This obeys PEP-440 specifiers:
    https://peps.python.org/pep-0440/#version-specifiers

    Some examples:

        >>> is_allowed_version('<=3.5', '3.3')
        True
        >>> is_allowed_version('<=3.2', '3.3')
        False
        >>> is_allowed_version('>3.2, <4.0', '3.3')
        True
    """
    pass

class TestDirective(SphinxDirective):
    """
    Base class for doctest-related directives.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

class TestsetupDirective(TestDirective):
    option_spec: ClassVar[OptionSpec] = {'skipif': directives.unchanged_required}

class TestcleanupDirective(TestDirective):
    option_spec: ClassVar[OptionSpec] = {'skipif': directives.unchanged_required}

class DoctestDirective(TestDirective):
    option_spec: ClassVar[OptionSpec] = {'hide': directives.flag, 'no-trim-doctest-flags': directives.flag, 'options': directives.unchanged, 'pyversion': directives.unchanged_required, 'skipif': directives.unchanged_required, 'trim-doctest-flags': directives.flag}

class TestcodeDirective(TestDirective):
    option_spec: ClassVar[OptionSpec] = {'hide': directives.flag, 'no-trim-doctest-flags': directives.flag, 'pyversion': directives.unchanged_required, 'skipif': directives.unchanged_required, 'trim-doctest-flags': directives.flag}

class TestoutputDirective(TestDirective):
    option_spec: ClassVar[OptionSpec] = {'hide': directives.flag, 'no-trim-doctest-flags': directives.flag, 'options': directives.unchanged, 'pyversion': directives.unchanged_required, 'skipif': directives.unchanged_required, 'trim-doctest-flags': directives.flag}
parser = doctest.DocTestParser()

class TestGroup:

    def __init__(self, name: str) -> None:
        self.name = name
        self.setup: list[TestCode] = []
        self.tests: list[list[TestCode] | tuple[TestCode, None]] = []
        self.cleanup: list[TestCode] = []

    def __repr__(self) -> str:
        return f'TestGroup(name={self.name!r}, setup={self.setup!r}, cleanup={self.cleanup!r}, tests={self.tests!r})'

class TestCode:

    def __init__(self, code: str, type: str, filename: str, lineno: int, options: dict | None=None) -> None:
        self.code = code
        self.type = type
        self.filename = filename
        self.lineno = lineno
        self.options = options or {}

    def __repr__(self) -> str:
        return f'TestCode({self.code!r}, {self.type!r}, filename={self.filename!r}, lineno={self.lineno!r}, options={self.options!r})'

class SphinxDocTestRunner(doctest.DocTestRunner):
    pass

class DocTestBuilder(Builder):
    """
    Runs test snippets in the documentation.
    """
    name = 'doctest'
    epilog = __('Testing of doctests in the sources finished, look at the results in %(outdir)s/output.txt.')

    def __del__(self) -> None:
        if hasattr(self, 'outfile'):
            self.outfile.close()

    def get_filename_for_node(self, node: Node, docname: str) -> str:
        """Try to get the file which actually contains the doctest, not the
        filename of the document it's included in.
        """
        pass

    @staticmethod
    def get_line_number(node: Node) -> int | None:
        """Get the real line number or admit we don't know."""
        pass