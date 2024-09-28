"""Format coloured console output."""
from __future__ import annotations
import os
import sys
from collections.abc import Callable
if sys.platform == 'win32':
    import colorama
_COLOURING_DISABLED = True

def terminal_supports_colour() -> bool:
    """Return True if coloured terminal output is supported."""
    pass
if sys.platform == 'win32':
    _create_input_mode_colour_func = _create_colour_func
reset = _create_colour_func('39;49;00')
bold = _create_colour_func('01')
faint = _create_colour_func('02')
standout = _create_colour_func('03')
underline = _create_colour_func('04')
blink = _create_colour_func('05')
black = _create_colour_func('30')
darkred = _create_colour_func('31')
darkgreen = _create_colour_func('32')
brown = _create_colour_func('33')
darkblue = _create_colour_func('34')
purple = _create_colour_func('35')
turquoise = _create_colour_func('36')
lightgray = _create_colour_func('37')
darkgray = _create_colour_func('90')
red = _create_colour_func('91')
green = _create_colour_func('92')
yellow = _create_colour_func('93')
blue = _create_colour_func('94')
fuchsia = _create_colour_func('95')
teal = _create_colour_func('96')
white = _create_colour_func('97')