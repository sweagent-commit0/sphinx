from __future__ import annotations
import re
import sys
import tempfile
from typing import TYPE_CHECKING, TextIO
from sphinx.errors import SphinxParallelError
if TYPE_CHECKING:
    from sphinx.application import Sphinx
_ANSI_COLOUR_CODES: re.Pattern[str] = re.compile('\x1b.*?m')

def terminal_safe(s: str, /) -> str:
    """Safely encode a string for printing to the terminal."""
    pass

def save_traceback(app: Sphinx | None, exc: BaseException) -> str:
    """Save the given exception's traceback in a temporary file."""
    pass