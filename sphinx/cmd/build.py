"""Build documentation from a provided source."""
from __future__ import annotations
import argparse
import bdb
import contextlib
import locale
import multiprocessing
import os
import pdb
import sys
import traceback
from os import path
from typing import TYPE_CHECKING, Any, TextIO
from docutils.utils import SystemMessage
import sphinx.locale
from sphinx import __display_version__
from sphinx.application import Sphinx
from sphinx.errors import SphinxError, SphinxParallelError
from sphinx.locale import __
from sphinx.util._io import TeeStripANSI
from sphinx.util.console import color_terminal, nocolor, red, terminal_safe
from sphinx.util.docutils import docutils_namespace, patch_docutils
from sphinx.util.exceptions import format_exception_cut_frames, save_traceback
from sphinx.util.osutil import ensuredir
if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Protocol

    class SupportsWrite(Protocol):
        pass

def jobs_argument(value: str) -> int:
    """
    Special type to handle 'auto' flags passed to 'sphinx-build' via -j flag. Can
    be expanded to handle other special scaling requests, such as setting job count
    to cpu_count.
    """
    pass

def make_main(argv: Sequence[str]) -> int:
    """Sphinx build "make mode" entry."""
    pass

def build_main(argv: Sequence[str]) -> int:
    """Sphinx build "main" command-line entry."""
    pass
if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))