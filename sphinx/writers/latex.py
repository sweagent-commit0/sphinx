"""Custom docutils writer for LaTeX.

Much of this code is adapted from Dave Kuhlman's "docpy" writer from his
docutils sandbox.
"""
from __future__ import annotations
import re
from collections import defaultdict
from collections.abc import Iterable
from os import path
from typing import TYPE_CHECKING, Any, cast
from docutils import nodes, writers
from sphinx import addnodes, highlighting
from sphinx.domains.std import StandardDomain
from sphinx.errors import SphinxError
from sphinx.locale import _, __, admonitionlabels
from sphinx.util import logging, texescape
from sphinx.util.docutils import SphinxTranslator
from sphinx.util.index_entries import split_index_msg
from sphinx.util.nodes import clean_astext, get_prev_node
from sphinx.util.template import LaTeXRenderer
from sphinx.util.texescape import tex_replace_map
try:
    from docutils.utils.roman import toRoman
except ImportError:
    from roman import toRoman
if TYPE_CHECKING:
    from docutils.nodes import Element, Node, Text
    from sphinx.builders.latex import LaTeXBuilder
    from sphinx.builders.latex.theming import Theme
    from sphinx.domains import IndexEntry
logger = logging.getLogger(__name__)
MAX_CITATION_LABEL_LENGTH = 8
LATEXSECTIONNAMES = ['part', 'chapter', 'section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']
ENUMERATE_LIST_STYLE = defaultdict(lambda: '\\arabic', {'arabic': '\\arabic', 'loweralpha': '\\alph', 'upperalpha': '\\Alph', 'lowerroman': '\\roman', 'upperroman': '\\Roman'})
CR = '\n'
BLANKLINE = '\n\n'
EXTRA_RE = re.compile('^(.*\\S)\\s+\\(([^()]*)\\)\\s*$')

class collected_footnote(nodes.footnote):
    """Footnotes that are collected are assigned this class."""

class UnsupportedError(SphinxError):
    category = 'Markup is unsupported in LaTeX'

class LaTeXWriter(writers.Writer):
    supported = ('sphinxlatex',)
    settings_spec = ('LaTeX writer options', '', (('Document name', ['--docname'], {'default': ''}), ('Document class', ['--docclass'], {'default': 'manual'}), ('Author', ['--author'], {'default': ''})))
    settings_defaults: dict[str, Any] = {}
    theme: Theme

    def __init__(self, builder: LaTeXBuilder) -> None:
        super().__init__()
        self.builder = builder

class Table:
    """A table data"""

    def __init__(self, node: Element) -> None:
        self.header: list[str] = []
        self.body: list[str] = []
        self.align = node.get('align', 'default')
        self.classes: list[str] = node.get('classes', [])
        self.styles: list[str] = []
        if 'standard' in self.classes:
            self.styles.append('standard')
        elif 'borderless' in self.classes:
            self.styles.append('borderless')
        elif 'booktabs' in self.classes:
            self.styles.append('booktabs')
        if 'nocolorrows' in self.classes:
            self.styles.append('nocolorrows')
        elif 'colorrows' in self.classes:
            self.styles.append('colorrows')
        self.colcount = 0
        self.colspec: str = ''
        if 'booktabs' in self.styles or 'borderless' in self.styles:
            self.colsep: str | None = ''
        elif 'standard' in self.styles:
            self.colsep = '|'
        else:
            self.colsep = None
        self.colwidths: list[int] = []
        self.has_problematic = False
        self.has_oldproblematic = False
        self.has_verbatim = False
        self.caption: list[str] = []
        self.stubs: list[int] = []
        self.col = 0
        self.row = 0
        self.cells: dict[tuple[int, int], int] = defaultdict(int)
        self.cell_id = 0

    def is_longtable(self) -> bool:
        """True if and only if table uses longtable environment."""
        pass

    def get_table_type(self) -> str:
        """Returns the LaTeX environment name for the table.

        The class currently supports:

        * longtable
        * tabular
        * tabulary
        """
        pass

    def get_colspec(self) -> str:
        """Returns a column spec of table.

        This is what LaTeX calls the 'preamble argument' of the used table environment.

        .. note::

           The ``\\\\X`` and ``T`` column type specifiers are defined in
           ``sphinxlatextables.sty``.
        """
        pass

    def add_cell(self, height: int, width: int) -> None:
        """Adds a new cell to a table.

        It will be located at current position: (``self.row``, ``self.col``).
        """
        pass

    def cell(self, row: int | None=None, col: int | None=None) -> TableCell | None:
        """Returns a cell object (i.e. rectangular area) containing given position.

        If no option arguments: ``row`` or ``col`` are given, the current position;
        ``self.row`` and ``self.col`` are used to get a cell object by default.
        """
        pass

class TableCell:
    """Data of a cell in a table."""

    def __init__(self, table: Table, row: int, col: int) -> None:
        if table.cells[row, col] == 0:
            raise IndexError
        self.table = table
        self.cell_id = table.cells[row, col]
        self.row = row
        self.col = col
        while table.cells[self.row - 1, self.col] == self.cell_id:
            self.row -= 1
        while table.cells[self.row, self.col - 1] == self.cell_id:
            self.col -= 1

    @property
    def width(self) -> int:
        """Returns the cell width."""
        pass

    @property
    def height(self) -> int:
        """Returns the cell height."""
        pass

def escape_abbr(text: str) -> str:
    """Adjust spacing after abbreviations."""
    pass

def rstdim_to_latexdim(width_str: str, scale: int=100) -> str:
    """Convert `width_str` with rst length to LaTeX length."""
    pass

class LaTeXTranslator(SphinxTranslator):
    builder: LaTeXBuilder
    secnumdepth = 2
    ignore_missing_images = False

    def __init__(self, document: nodes.document, builder: LaTeXBuilder, theme: Theme) -> None:
        super().__init__(document, builder)
        self.body: list[str] = []
        self.theme = theme
        self.in_title = 0
        self.in_production_list = 0
        self.in_footnote = 0
        self.in_caption = 0
        self.in_term = 0
        self.needs_linetrimming = 0
        self.in_minipage = 0
        self.no_latex_floats = 0
        self.first_document = 1
        self.this_is_the_title = 1
        self.literal_whitespace = 0
        self.in_parsed_literal = 0
        self.compact_list = 0
        self.first_param = 0
        self.in_desc_signature = False
        sphinxpkgoptions = []
        self.elements = self.builder.context.copy()
        self.sectionnames = LATEXSECTIONNAMES.copy()
        if self.theme.toplevel_sectioning == 'section':
            self.sectionnames.remove('chapter')
        self.top_sectionlevel = 1
        if self.config.latex_toplevel_sectioning:
            try:
                self.top_sectionlevel = self.sectionnames.index(self.config.latex_toplevel_sectioning)
            except ValueError:
                logger.warning(__('unknown %r toplevel_sectioning for class %r'), self.config.latex_toplevel_sectioning, self.theme.docclass)
        if self.config.numfig:
            self.numfig_secnum_depth = self.config.numfig_secnum_depth
            if self.numfig_secnum_depth > 0:
                if len(self.sectionnames) < len(LATEXSECTIONNAMES) and self.top_sectionlevel > 0:
                    self.numfig_secnum_depth += self.top_sectionlevel
                else:
                    self.numfig_secnum_depth += self.top_sectionlevel - 1
                self.numfig_secnum_depth = min(self.numfig_secnum_depth, len(LATEXSECTIONNAMES) - 1)
                sphinxpkgoptions.append('numfigreset=%s' % self.numfig_secnum_depth)
            else:
                sphinxpkgoptions.append('nonumfigreset')
        if self.config.numfig and self.config.math_numfig:
            sphinxpkgoptions.extend(['mathnumfig', 'mathnumsep={%s}' % self.config.math_numsep])
        if self.config.language not in {'en', 'ja'} and 'fncychap' not in self.config.latex_elements:
            self.elements['fncychap'] = '\\usepackage[Sonny]{fncychap}' + CR + '\\ChNameVar{\\Large\\normalfont\\sffamily}' + CR + '\\ChTitleVar{\\Large\\normalfont\\sffamily}'
        self.babel = self.builder.babel
        if not self.babel.is_supported_language():
            logger.warning(__('no Babel option known for language %r'), self.config.language)
        minsecnumdepth = self.secnumdepth
        if self.document.get('tocdepth'):
            tocdepth = self.document.get('tocdepth', 999) + self.top_sectionlevel - 2
            if len(self.sectionnames) < len(LATEXSECTIONNAMES) and self.top_sectionlevel > 0:
                tocdepth += 1
            if tocdepth > len(LATEXSECTIONNAMES) - 2:
                logger.warning(__('too large :maxdepth:, ignored.'))
                tocdepth = len(LATEXSECTIONNAMES) - 2
            self.elements['tocdepth'] = '\\setcounter{tocdepth}{%d}' % tocdepth
            minsecnumdepth = max(minsecnumdepth, tocdepth)
        if self.config.numfig and self.config.numfig_secnum_depth > 0:
            minsecnumdepth = max(minsecnumdepth, self.numfig_secnum_depth - 1)
        if minsecnumdepth > self.secnumdepth:
            self.elements['secnumdepth'] = '\\setcounter{secnumdepth}{%d}' % minsecnumdepth
        contentsname = document.get('contentsname')
        if contentsname:
            self.elements['contentsname'] = self.babel_renewcommand('\\contentsname', contentsname)
        if self.elements['maxlistdepth']:
            sphinxpkgoptions.append('maxlistdepth=%s' % self.elements['maxlistdepth'])
        if sphinxpkgoptions:
            self.elements['sphinxpkgoptions'] = '[,%s]' % ','.join(sphinxpkgoptions)
        if self.elements['sphinxsetup']:
            self.elements['sphinxsetup'] = '\\sphinxsetup{%s}' % self.elements['sphinxsetup']
        if self.elements['extraclassoptions']:
            self.elements['classoptions'] += ',' + self.elements['extraclassoptions']
        self.highlighter = highlighting.PygmentsBridge('latex', self.config.pygments_style, latex_engine=self.config.latex_engine)
        self.context: list[Any] = []
        self.descstack: list[str] = []
        self.tables: list[Table] = []
        self.next_table_colspec: str | None = None
        self.bodystack: list[list[str]] = []
        self.footnote_restricted: Element | None = None
        self.pending_footnotes: list[nodes.footnote_reference] = []
        self.curfilestack: list[str] = []
        self.handled_abbrs: set[str] = set()

    @property
    def table(self) -> Table | None:
        """Get current table."""
        pass
    depart_sidebar = depart_topic

    def _visit_sig_parameter_list(self, node: Element, parameter_group: type[Element]) -> None:
        """Visit a signature parameters or type parameters list.

        The *parameter_group* value is the type of a child node acting as a required parameter
        or as a set of contiguous optional parameters.

        The caller is responsible for closing adding surrounding LaTeX macro argument start
        and stop tokens.
        """
        pass
    visit_field_name = visit_term
    depart_field_name = depart_term
    visit_field_body = visit_definition
    depart_field_body = depart_definition

    def is_inline(self, node: Element) -> bool:
        """Check whether a node represents an inline element."""
        pass
    visit_attention = _visit_named_admonition
    depart_attention = _depart_named_admonition
    visit_caution = _visit_named_admonition
    depart_caution = _depart_named_admonition
    visit_danger = _visit_named_admonition
    depart_danger = _depart_named_admonition
    visit_error = _visit_named_admonition
    depart_error = _depart_named_admonition
    visit_hint = _visit_named_admonition
    depart_hint = _depart_named_admonition
    visit_important = _visit_named_admonition
    depart_important = _depart_named_admonition
    visit_note = _visit_named_admonition
    depart_note = _depart_named_admonition
    visit_tip = _visit_named_admonition
    depart_tip = _depart_named_admonition
    visit_warning = _visit_named_admonition
    depart_warning = _depart_named_admonition
    visit_doctest_block = visit_literal_block
    depart_doctest_block = depart_literal_block

    def visit_option_argument(self, node: Element) -> None:
        """The delimiter between an option and its argument."""
        pass
from sphinx.builders.latex.nodes import HYPERLINK_SUPPORT_NODES, captioned_literal_block, footnotetext