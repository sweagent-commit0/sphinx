"""sphinx-build -M command-line handling.

This replaces the old, platform-dependent and once-generated content
of Makefile / make.bat.

This is in its own module so that importing it is fast.  It should not
import the main Sphinx modules (like sphinx.applications, sphinx.builders).
"""
from __future__ import annotations
import os
import subprocess
import sys
from os import path
from typing import TYPE_CHECKING
import sphinx
from sphinx.cmd.build import build_main
from sphinx.util.console import blue, bold, color_terminal, nocolor
from sphinx.util.osutil import rmtree
if sys.version_info >= (3, 11):
    from contextlib import chdir
else:
    from sphinx.util.osutil import _chdir as chdir
if TYPE_CHECKING:
    from collections.abc import Sequence
BUILDERS = [('', 'html', 'to make standalone HTML files'), ('', 'dirhtml', 'to make HTML files named index.html in directories'), ('', 'singlehtml', 'to make a single large HTML file'), ('', 'pickle', 'to make pickle files'), ('', 'json', 'to make JSON files'), ('', 'htmlhelp', 'to make HTML files and an HTML help project'), ('', 'qthelp', 'to make HTML files and a qthelp project'), ('', 'devhelp', 'to make HTML files and a Devhelp project'), ('', 'epub', 'to make an epub'), ('', 'latex', 'to make LaTeX files, you can set PAPER=a4 or PAPER=letter'), ('posix', 'latexpdf', 'to make LaTeX and PDF files (default pdflatex)'), ('posix', 'latexpdfja', 'to make LaTeX files and run them through platex/dvipdfmx'), ('', 'text', 'to make text files'), ('', 'man', 'to make manual pages'), ('', 'texinfo', 'to make Texinfo files'), ('posix', 'info', 'to make Texinfo files and run them through makeinfo'), ('', 'gettext', 'to make PO message catalogs'), ('', 'changes', 'to make an overview of all changed/added/deprecated items'), ('', 'xml', 'to make Docutils-native XML files'), ('', 'pseudoxml', 'to make pseudoxml-XML files for display purposes'), ('', 'linkcheck', 'to check all external links for integrity'), ('', 'doctest', 'to run all doctests embedded in the documentation (if enabled)'), ('', 'coverage', 'to run coverage check of the documentation (if enabled)'), ('', 'clean', 'to remove everything in the build directory')]

class Make:

    def __init__(self, *, source_dir: str, build_dir: str, opts: Sequence[str]) -> None:
        self.source_dir = source_dir
        self.build_dir = build_dir
        self.opts = [*opts]