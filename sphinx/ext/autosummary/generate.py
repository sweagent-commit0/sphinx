"""Generates reST source files for autosummary.

Usable as a library or script to generate automatic RST source files for
items referred to in autosummary:: directives.

Each generated RST file contains a single auto*:: directive which
extracts the docstring of the referred item.

Example Makefile rule::

   generate:
           sphinx-autogen -o source/generated source/*.rst
"""
from __future__ import annotations
import argparse
import importlib
import inspect
import locale
import os
import pkgutil
import pydoc
import re
import sys
from os import path
from pathlib import Path
from typing import TYPE_CHECKING, Any, NamedTuple
from jinja2 import TemplateNotFound
from jinja2.sandbox import SandboxedEnvironment
import sphinx.locale
from sphinx import __display_version__, package_dir
from sphinx.builders import Builder
from sphinx.config import Config
from sphinx.errors import PycodeError
from sphinx.ext.autodoc.importer import import_module
from sphinx.ext.autosummary import ImportExceptionGroup, get_documenter, import_by_name, import_ivar_by_name
from sphinx.locale import __
from sphinx.pycode import ModuleAnalyzer
from sphinx.registry import SphinxComponentRegistry
from sphinx.util import logging, rst
from sphinx.util.inspect import getall, safe_getattr
from sphinx.util.osutil import ensuredir
from sphinx.util.template import SphinxTemplateLoader
if TYPE_CHECKING:
    from collections.abc import Sequence, Set
    from gettext import NullTranslations
    from sphinx.application import Sphinx
    from sphinx.ext.autodoc import Documenter
logger = logging.getLogger(__name__)

class DummyApplication:
    """Dummy Application class for sphinx-autogen command."""

    def __init__(self, translator: NullTranslations) -> None:
        self.config = Config()
        self.registry = SphinxComponentRegistry()
        self.messagelog: list[str] = []
        self.srcdir = '/'
        self.translator = translator
        self.verbosity = 0
        self._warncount = 0
        self._exception_on_warning = False
        self.config.add('autosummary_context', {}, 'env', ())
        self.config.add('autosummary_filename_map', {}, 'env', ())
        self.config.add('autosummary_ignore_module_all', True, 'env', bool)

class AutosummaryEntry(NamedTuple):
    name: str
    path: str | None
    template: str
    recursive: bool

class AutosummaryRenderer:
    """A helper class for rendering."""

    def __init__(self, app: Sphinx) -> None:
        if isinstance(app, Builder):
            msg = 'Expected a Sphinx application object!'
            raise ValueError(msg)
        system_templates_path = [os.path.join(package_dir, 'ext', 'autosummary', 'templates')]
        loader = SphinxTemplateLoader(app.srcdir, app.config.templates_path, system_templates_path)
        self.env = SandboxedEnvironment(loader=loader)
        self.env.filters['escape'] = rst.escape
        self.env.filters['e'] = rst.escape
        self.env.filters['underline'] = _underline
        if app.translator:
            self.env.add_extension('jinja2.ext.i18n')
            self.env.install_gettext_translations(app.translator)

    def render(self, template_name: str, context: dict[str, Any]) -> str:
        """Render a template file."""
        pass

def _split_full_qualified_name(name: str) -> tuple[str | None, str]:
    """Split full qualified name to a pair of modname and qualname.

    A qualname is an abbreviation for "Qualified name" introduced at PEP-3155
    (https://peps.python.org/pep-3155/).  It is a dotted path name
    from the module top-level.

    A "full" qualified name means a string containing both module name and
    qualified name.

    .. note:: This function actually imports the module to check its existence.
              Therefore you need to mock 3rd party modules if needed before
              calling this function.
    """
    pass

class ModuleScanner:

    def __init__(self, app: Any, obj: Any) -> None:
        self.app = app
        self.object = obj

def members_of(obj: Any, conf: Config) -> Sequence[str]:
    """Get the members of ``obj``, possibly ignoring the ``__all__`` module attribute

    Follows the ``conf.autosummary_ignore_module_all`` setting.
    """
    pass

def _get_module_attrs(name: str, members: Any) -> tuple[list[str], list[str]]:
    """Find module attributes with docstrings."""
    pass

def generate_autosummary_docs(sources: list[str], output_dir: str | os.PathLike[str] | None=None, suffix: str='.rst', base_path: str | os.PathLike[str] | None=None, imported_members: bool=False, app: Sphinx | None=None, overwrite: bool=True, encoding: str='utf-8') -> list[Path]:
    """Generate autosummary documentation for the given sources.

    :returns: list of generated files (both new and existing ones)
    """
    pass

def find_autosummary_in_files(filenames: list[str]) -> list[AutosummaryEntry]:
    """Find out what items are documented in source/*.rst.

    See `find_autosummary_in_lines`.
    """
    pass

def find_autosummary_in_docstring(name: str, filename: str | None=None) -> list[AutosummaryEntry]:
    """Find out what items are documented in the given object's docstring.

    See `find_autosummary_in_lines`.
    """
    pass

def find_autosummary_in_lines(lines: list[str], module: str | None=None, filename: str | None=None) -> list[AutosummaryEntry]:
    """Find out what items appear in autosummary:: directives in the
    given lines.

    Returns a list of (name, toctree, template) where *name* is a name
    of an object and *toctree* the :toctree: path of the corresponding
    autosummary directive (relative to the root of the file name), and
    *template* the value of the :template: option. *toctree* and
    *template* ``None`` if the directive does not have the
    corresponding options set.
    """
    pass
if __name__ == '__main__':
    main(sys.argv[1:])