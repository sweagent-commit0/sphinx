"""Quickly setup documentation source to work with Sphinx."""
from __future__ import annotations
import argparse
import locale
import os
import sys
import time
from os import path
from typing import TYPE_CHECKING, Any
try:
    import readline
    if TYPE_CHECKING and sys.platform == 'win32':
        raise ImportError
    READLINE_AVAILABLE = True
    if readline.__doc__ and 'libedit' in readline.__doc__:
        readline.parse_and_bind('bind ^I rl_complete')
        USE_LIBEDIT = True
    else:
        readline.parse_and_bind('tab: complete')
        USE_LIBEDIT = False
except ImportError:
    READLINE_AVAILABLE = False
    USE_LIBEDIT = False
from docutils.utils import column_width
import sphinx.locale
from sphinx import __display_version__, package_dir
from sphinx.locale import __
from sphinx.util.console import bold, color_terminal, colorize, nocolor, red
from sphinx.util.osutil import ensuredir
from sphinx.util.template import SphinxRenderer
if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
EXTENSIONS = {'autodoc': __('automatically insert docstrings from modules'), 'doctest': __('automatically test code snippets in doctest blocks'), 'intersphinx': __('link between Sphinx documentation of different projects'), 'todo': __('write "todo" entries that can be shown or hidden on build'), 'coverage': __('checks for documentation coverage'), 'imgmath': __('include math, rendered as PNG or SVG images'), 'mathjax': __('include math, rendered in the browser by MathJax'), 'ifconfig': __('conditional inclusion of content based on config values'), 'viewcode': __('include links to the source code of documented Python objects'), 'githubpages': __('create .nojekyll file to publish the document on GitHub pages')}
DEFAULTS = {'path': '.', 'sep': False, 'dot': '_', 'language': None, 'suffix': '.rst', 'master': 'index', 'makefile': True, 'batchfile': True}
PROMPT_PREFIX = '> '
if sys.platform == 'win32':
    COLOR_QUESTION = 'bold'
else:
    COLOR_QUESTION = 'purple'

class ValidationError(Exception):
    """Raised for validation errors."""

class QuickstartRenderer(SphinxRenderer):

    def __init__(self, templatedir: str='') -> None:
        self.templatedir = templatedir
        super().__init__()

    def _has_custom_template(self, template_name: str) -> bool:
        """Check if custom template file exists.

        Note: Please don't use this function from extensions.
              It will be removed in the future without deprecation period.
        """
        pass

def ask_user(d: dict[str, Any]) -> None:
    """Ask the user for quickstart values missing from *d*.

    Values are:

    * path:      root path
    * sep:       separate source and build dirs (bool)
    * dot:       replacement for dot in _templates etc.
    * project:   project name
    * author:    author names
    * version:   version of project
    * release:   release of project
    * language:  document language
    * suffix:    source file suffix
    * master:    master document name
    * extensions:  extensions to use (list)
    * makefile:  make Makefile
    * batchfile: make command file
    """
    pass

def generate(d: dict[str, Any], overwrite: bool=True, silent: bool=False, templatedir: str | None=None) -> None:
    """Generate project based on values in *d*."""
    pass
if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))