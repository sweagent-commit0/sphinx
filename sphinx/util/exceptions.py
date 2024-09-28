from __future__ import annotations
import sys
import traceback
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING
from sphinx.errors import SphinxParallelError
from sphinx.util.console import strip_escape_sequences
if TYPE_CHECKING:
    from sphinx.application import Sphinx

def save_traceback(app: Sphinx | None, exc: BaseException) -> str:
    """Save the given exception's traceback in a temporary file."""
    pass

def format_exception_cut_frames(x: int=1) -> str:
    """Format an exception with traceback, but only the last x frames."""
    pass