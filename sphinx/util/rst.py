"""reST helper functions."""
from __future__ import annotations
import re
from collections import defaultdict
from contextlib import contextmanager
from typing import TYPE_CHECKING, cast
from unicodedata import east_asian_width
from docutils.parsers.rst import roles
from docutils.parsers.rst.languages import en as english
from docutils.parsers.rst.states import Body
from docutils.utils import Reporter
from jinja2 import Environment, pass_environment
from sphinx.locale import __
from sphinx.util import docutils, logging
if TYPE_CHECKING:
    from collections.abc import Iterator
    from docutils.statemachine import StringList
logger = logging.getLogger(__name__)
FIELD_NAME_RE = re.compile(Body.patterns['field_marker'])
symbols_re = re.compile('([!-\\-/:-@\\[-`{-~])')
SECTIONING_CHARS = ['=', '-', '~']
WIDECHARS: dict[str, str] = defaultdict(lambda: 'WF')
WIDECHARS['ja'] = 'WFA'

def textwidth(text: str, widechars: str='WF') -> int:
    """Get width of text."""
    pass

@pass_environment
def heading(env: Environment, text: str, level: int=1) -> str:
    """Create a heading for *level*."""
    pass

def prepend_prolog(content: StringList, prolog: str) -> None:
    """Prepend a string to content body as prolog."""
    pass

def append_epilog(content: StringList, epilog: str) -> None:
    """Append a string to content body as epilog."""
    pass