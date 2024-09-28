"""Creates reST files corresponding to Python modules for code documentation.

Parses a directory tree looking for Python modules and packages and creates
ReST files appropriately to create code documentation with Sphinx.  It also
creates a modules index (named modules.<suffix>).

This is derived from the "sphinx-autopackage" script, which is:
Copyright 2008 Société des arts technologiques (SAT),
https://sat.qc.ca/
"""
from __future__ import annotations
import argparse
import fnmatch
import glob
import locale
import os
import re
import sys
from copy import copy
from importlib.machinery import EXTENSION_SUFFIXES
from os import path
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol
import sphinx.locale
from sphinx import __display_version__, package_dir
from sphinx.cmd.quickstart import EXTENSIONS
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.osutil import FileAvoidWrite, ensuredir
from sphinx.util.template import ReSTRenderer
if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
logger = logging.getLogger(__name__)
if 'SPHINX_APIDOC_OPTIONS' in os.environ:
    OPTIONS = os.environ['SPHINX_APIDOC_OPTIONS'].split(',')
else:
    OPTIONS = ['members', 'undoc-members', 'show-inheritance']
PY_SUFFIXES = ('.py', '.pyx', *tuple(EXTENSION_SUFFIXES))
template_dir = path.join(package_dir, 'templates', 'apidoc')

def is_initpy(filename: str | Path) -> bool:
    """Check *filename* is __init__ file or not."""
    pass

def module_join(*modnames: str | None) -> str:
    """Join module names with dots."""
    pass

def is_packagedir(dirname: str | None=None, files: list[str] | None=None) -> bool:
    """Check given *files* contains __init__ file."""
    pass

def write_file(name: str, text: str, opts: CliOptions) -> Path:
    """Write the output file for module/package <name>."""
    pass

def create_module_file(package: str | None, basename: str, opts: CliOptions, user_template_dir: str | None=None) -> Path:
    """Build the text of the file and write the file."""
    pass

def create_package_file(root: str, master_package: str | None, subroot: str, py_files: list[str], opts: CliOptions, subs: list[str], is_namespace: bool, excludes: Sequence[re.Pattern[str]]=(), user_template_dir: str | None=None) -> list[Path]:
    """Build the text of the file and write the file.

    Also create submodules if necessary.

    :returns: list of written files
    """
    pass

def create_modules_toc_file(modules: list[str], opts: CliOptions, name: str='modules', user_template_dir: str | None=None) -> Path:
    """Create the module's index."""
    pass

def is_skipped_package(dirname: str | Path, opts: CliOptions, excludes: Sequence[re.Pattern[str]]=()) -> bool:
    """Check if we want to skip this module."""
    pass

def is_skipped_module(filename: str | Path, opts: CliOptions, _excludes: Sequence[re.Pattern[str]]) -> bool:
    """Check if we want to skip this module."""
    pass

def walk(rootpath: str, excludes: Sequence[re.Pattern[str]], opts: CliOptions) -> Iterator[tuple[str, list[str], list[str]]]:
    """Walk through the directory and list files and subdirectories up."""
    pass

def has_child_module(rootpath: str, excludes: Sequence[re.Pattern[str]], opts: CliOptions) -> bool:
    """Check the given directory contains child module/s (at least one)."""
    pass

def recurse_tree(rootpath: str, excludes: Sequence[re.Pattern[str]], opts: CliOptions, user_template_dir: str | None=None) -> tuple[list[Path], list[str]]:
    """
    Look for every file in the directory tree and create the corresponding
    ReST files.
    """
    pass

def is_excluded(root: str | Path, excludes: Sequence[re.Pattern[str]]) -> bool:
    """Check if the directory is in the exclude list.

    Note: by having trailing slashes, we avoid common prefix issues, like
          e.g. an exclude "foo" also accidentally excluding "foobar".
    """
    pass

class CliOptions(Protocol):
    """Arguments parsed from the command line."""
    module_path: str
    exclude_pattern: list[str]
    destdir: str
    quiet: bool
    maxdepth: int
    force: bool
    followlinks: bool
    dryrun: bool
    separatemodules: bool
    includeprivate: bool
    tocfile: str
    noheadings: bool
    modulefirst: bool
    implicit_namespaces: bool
    suffix: str
    full: bool
    append_syspath: bool
    header: str | None
    author: str | None
    version: str | None
    release: str | None
    extensions: list[str] | None
    templatedir: str | None
    remove_old: bool

def main(argv: Sequence[str]=(), /) -> int:
    """Parse and check the command line arguments."""
    pass
if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))