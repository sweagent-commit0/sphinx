"""Custom docutils writer for plain text."""
from __future__ import annotations
import math
import os
import re
import textwrap
from collections.abc import Iterable, Iterator, Sequence
from itertools import chain, groupby, pairwise
from typing import TYPE_CHECKING, Any, cast
from docutils import nodes, writers
from docutils.utils import column_width
from sphinx import addnodes
from sphinx.locale import _, admonitionlabels
from sphinx.util.docutils import SphinxTranslator
if TYPE_CHECKING:
    from docutils.nodes import Element, Text
    from sphinx.builders.text import TextBuilder

class Cell:
    """Represents a cell in a table.
    It can span multiple columns or multiple lines.
    """

    def __init__(self, text: str='', rowspan: int=1, colspan: int=1) -> None:
        self.text = text
        self.wrapped: list[str] = []
        self.rowspan = rowspan
        self.colspan = colspan
        self.col: int | None = None
        self.row: int | None = None

    def __repr__(self) -> str:
        return f'<Cell {self.text!r} {self.row}v{self.rowspan}/{self.col}>{self.colspan}>'

    def __hash__(self) -> int:
        return hash((self.col, self.row))

    def __bool__(self) -> bool:
        return self.text != '' and self.col is not None and (self.row is not None)

class Table:
    """Represents a table, handling cells that can span multiple lines
    or rows, like::

       +-----------+-----+
       | AAA       | BBB |
       +-----+-----+     |
       |     | XXX |     |
       |     +-----+-----+
       | DDD | CCC       |
       +-----+-----------+

    This class can be used in two ways, either:

    - With absolute positions: call ``table[line, col] = Cell(...)``,
      this overwrites any existing cell(s) at these positions.

    - With relative positions: call the ``add_row()`` and
      ``add_cell(Cell(...))`` as needed.

    Cells spanning multiple rows or multiple columns (having a
    colspan or rowspan greater than one) are automatically referenced
    by all the table cells they cover. This is a useful
    representation as we can simply check
    ``if self[x, y] is self[x, y+1]`` to recognize a rowspan.

    Colwidth is not automatically computed, it has to be given, either
    at construction time, or during the table construction.

    Example usage::

       table = Table([6, 6])
       table.add_cell(Cell("foo"))
       table.add_cell(Cell("bar"))
       table.set_separator()
       table.add_row()
       table.add_cell(Cell("FOO"))
       table.add_cell(Cell("BAR"))
       print(table)
       +--------+--------+
       | foo    | bar    |
       |========|========|
       | FOO    | BAR    |
       +--------+--------+

    """

    def __init__(self, colwidth: list[int] | None=None) -> None:
        self.lines: list[list[Cell]] = []
        self.separator = 0
        self.colwidth: list[int] = colwidth if colwidth is not None else []
        self.current_line = 0
        self.current_col = 0

    def add_row(self) -> None:
        """Add a row to the table, to use with ``add_cell()``.  It is not needed
        to call ``add_row()`` before the first ``add_cell()``.
        """
        pass

    def set_separator(self) -> None:
        """Sets the separator below the current line."""
        pass

    def add_cell(self, cell: Cell) -> None:
        """Add a cell to the current line, to use with ``add_row()``.  To add
        a cell spanning multiple lines or rows, simply set the
        ``cell.colspan`` or ``cell.rowspan`` BEFORE inserting it into
        the table.
        """
        pass

    def __getitem__(self, pos: tuple[int, int]) -> Cell:
        line, col = pos
        self._ensure_has_line(line + 1)
        self._ensure_has_column(col + 1)
        return self.lines[line][col]

    def __setitem__(self, pos: tuple[int, int], cell: Cell) -> None:
        line, col = pos
        self._ensure_has_line(line + cell.rowspan)
        self._ensure_has_column(col + cell.colspan)
        for dline in range(cell.rowspan):
            for dcol in range(cell.colspan):
                self.lines[line + dline][col + dcol] = cell
                cell.row = line
                cell.col = col

    def __repr__(self) -> str:
        return '\n'.join(map(repr, self.lines))

    def cell_width(self, cell: Cell, source: list[int]) -> int:
        """Give the cell width, according to the given source (either
        ``self.colwidth`` or ``self.measured_widths``).
        This takes into account cells spanning multiple columns.
        """
        pass

    def rewrap(self) -> None:
        """Call ``cell.wrap()`` on all cells, and measure each column width
        after wrapping (result written in ``self.measured_widths``).
        """
        pass

    def physical_lines_for_line(self, line: list[Cell]) -> int:
        """For a given line, compute the number of physical lines it spans
        due to text wrapping.
        """
        pass

    def __str__(self) -> str:
        out = []
        self.rewrap()

        def writesep(char: str='-', lineno: int | None=None) -> str:
            """Called on the line *before* lineno.
            Called with no *lineno* for the last sep.
            """
            out: list[str] = []
            for colno, width in enumerate(self.measured_widths):
                if lineno is not None and lineno > 0 and (self[lineno, colno] is self[lineno - 1, colno]):
                    out.append(' ' * (width + 2))
                else:
                    out.append(char * (width + 2))
            head = '+' if out[0][0] == '-' else '|'
            tail = '+' if out[-1][0] == '-' else '|'
            glue = ['+' if left[0] == '-' or right[0] == '-' else '|' for left, right in pairwise(out)]
            glue.append(tail)
            return head + ''.join(chain.from_iterable(zip(out, glue, strict=False)))
        for lineno, line in enumerate(self.lines):
            if self.separator and lineno == self.separator:
                out.append(writesep('=', lineno))
            else:
                out.append(writesep('-', lineno))
            for physical_line in range(self.physical_lines_for_line(line)):
                linestr = ['|']
                for colno, cell in enumerate(line):
                    if cell.col != colno:
                        continue
                    if lineno != cell.row:
                        physical_text = ''
                    elif physical_line >= len(cell.wrapped):
                        physical_text = ''
                    else:
                        physical_text = cell.wrapped[physical_line]
                    adjust_len = len(physical_text) - column_width(physical_text)
                    linestr.append(' ' + physical_text.ljust(self.cell_width(cell, self.measured_widths) + 1 + adjust_len) + '|')
                out.append(''.join(linestr))
        out.append(writesep('-'))
        return '\n'.join(out)

class TextWrapper(textwrap.TextWrapper):
    """Custom subclass that uses a different word separator regex."""
    wordsep_re = re.compile('(\\s+|(?<=\\s)(?::[a-z-]+:)?`\\S+|[^\\s\\w]*\\w+[a-zA-Z]-(?=\\w+[a-zA-Z])|(?<=[\\w\\!\\"\\\'\\&\\.\\,\\?])-{2,}(?=\\w))')

    def _wrap_chunks(self, chunks: list[str]) -> list[str]:
        """The original _wrap_chunks uses len() to calculate width.

        This method respects wide/fullwidth characters for width adjustment.
        """
        pass

    def _break_word(self, word: str, space_left: int) -> tuple[str, str]:
        """Break line by unicode width instead of len(word)."""
        pass

    def _split(self, text: str) -> list[str]:
        """Override original method that only split by 'wordsep_re'.

        This '_split' splits wide-characters into chunks by one character.
        """
        pass

    def _handle_long_word(self, reversed_chunks: list[str], cur_line: list[str], cur_len: int, width: int) -> None:
        """Override original method for using self._break_word() instead of slice."""
        pass
MAXWIDTH = 70
STDINDENT = 3

class TextWriter(writers.Writer):
    supported = ('text',)
    settings_spec = ('No options here.', '', ())
    settings_defaults: dict[str, Any] = {}
    output: str

    def __init__(self, builder: TextBuilder) -> None:
        super().__init__()
        self.builder = builder

class TextTranslator(SphinxTranslator):
    builder: TextBuilder

    def __init__(self, document: nodes.document, builder: TextBuilder) -> None:
        super().__init__(document, builder)
        newlines = self.config.text_newlines
        if newlines == 'windows':
            self.nl = '\r\n'
        elif newlines == 'native':
            self.nl = os.linesep
        else:
            self.nl = '\n'
        self.sectionchars = self.config.text_sectionchars
        self.add_secnumbers = self.config.text_add_secnumbers
        self.secnumber_suffix = self.config.text_secnumber_suffix
        self.states: list[list[tuple[int, str | list[str]]]] = [[]]
        self.stateindent = [0]
        self.list_counter: list[int] = []
        self.sectionlevel = 0
        self.lineblocklevel = 0
        self.table: Table
        self.context: list[str] = []
        'Heterogeneous stack.\n\n        Used by visit_* and depart_* functions in conjunction with the tree\n        traversal. Make sure that the pops correspond to the pushes.\n        '
    visit_sidebar = visit_topic
    depart_sidebar = depart_topic

    def _visit_sig_parameter_list(self, node: Element, parameter_group: type[Element], sig_open_paren: str, sig_close_paren: str) -> None:
        """Visit a signature parameters or type parameters list.

        The *parameter_group* value is the type of a child node acting as a required parameter
        or as a set of contiguous optional parameters.
        """
        pass
    visit_attention = _visit_admonition
    depart_attention = _depart_admonition
    visit_caution = _visit_admonition
    depart_caution = _depart_admonition
    visit_danger = _visit_admonition
    depart_danger = _depart_admonition
    visit_error = _visit_admonition
    depart_error = _depart_admonition
    visit_hint = _visit_admonition
    depart_hint = _depart_admonition
    visit_important = _visit_admonition
    depart_important = _depart_admonition
    visit_note = _visit_admonition
    depart_note = _depart_admonition
    visit_tip = _visit_admonition
    depart_tip = _depart_admonition
    visit_warning = _visit_admonition
    depart_warning = _depart_admonition
    visit_seealso = _visit_admonition
    depart_seealso = _depart_admonition