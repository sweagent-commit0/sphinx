"""Highlight code blocks using Pygments."""
from __future__ import annotations
from functools import partial
from importlib import import_module
from typing import TYPE_CHECKING, Any
import pygments
from pygments import highlight
from pygments.filters import ErrorToken
from pygments.formatters import HtmlFormatter, LatexFormatter
from pygments.lexers import CLexer, PythonConsoleLexer, PythonLexer, RstLexer, TextLexer, get_lexer_by_name, guess_lexer
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound
from sphinx.locale import __
from sphinx.pygments_styles import NoneStyle, SphinxStyle
from sphinx.util import logging, texescape
if TYPE_CHECKING:
    from pygments.formatter import Formatter
    from pygments.lexer import Lexer
    from pygments.style import Style
if tuple(map(int, pygments.__version__.split('.')))[:2] < (2, 18):
    from pygments.formatter import Formatter
    Formatter.__class_getitem__ = classmethod(lambda cls, name: cls)
logger = logging.getLogger(__name__)
lexers: dict[str, Lexer] = {}
lexer_classes: dict[str, type[Lexer] | partial[Lexer]] = {'none': partial(TextLexer, stripnl=False), 'python': partial(PythonLexer, stripnl=False), 'pycon': partial(PythonConsoleLexer, stripnl=False), 'rest': partial(RstLexer, stripnl=False), 'c': partial(CLexer, stripnl=False)}
escape_hl_chars = {ord('\\'): '\\PYGZbs{}', ord('{'): '\\PYGZob{}', ord('}'): '\\PYGZcb{}'}
_LATEX_ADD_STYLES = '\n% Sphinx redefinitions\n% Originally to obtain a straight single quote via package textcomp, then\n% to fix problems for the 5.0.0 inline code highlighting (captions!).\n% The \\text is from amstext, a dependency of sphinx.sty.  It is here only\n% to avoid build errors if for some reason expansion is in math mode.\n\\def\\PYGZbs{\\text\\textbackslash}\n\\def\\PYGZus{\\_}\n\\def\\PYGZob{\\{}\n\\def\\PYGZcb{\\}}\n\\def\\PYGZca{\\text\\textasciicircum}\n\\def\\PYGZam{\\&}\n\\def\\PYGZlt{\\text\\textless}\n\\def\\PYGZgt{\\text\\textgreater}\n\\def\\PYGZsh{\\#}\n\\def\\PYGZpc{\\%}\n\\def\\PYGZdl{\\$}\n\\def\\PYGZhy{\\sphinxhyphen}% defined in sphinxlatexstyletext.sty\n\\def\\PYGZsq{\\text\\textquotesingle}\n\\def\\PYGZdq{"}\n\\def\\PYGZti{\\text\\textasciitilde}\n\\makeatletter\n% use \\protected to allow syntax highlighting in captions\n\\protected\\def\\PYG#1#2{\\PYG@reset\\PYG@toks#1+\\relax+{\\PYG@do{#2}}}\n\\makeatother\n'

class PygmentsBridge:
    html_formatter = HtmlFormatter[str]
    latex_formatter = LatexFormatter[str]

    def __init__(self, dest: str='html', stylename: str='sphinx', latex_engine: str | None=None) -> None:
        self.dest = dest
        self.latex_engine = latex_engine
        style = self.get_style(stylename)
        self.formatter_args: dict[str, Any] = {'style': style}
        if dest == 'html':
            self.formatter: type[Formatter[str]] = self.html_formatter
        else:
            self.formatter = self.latex_formatter
            self.formatter_args['commandprefix'] = 'PYG'