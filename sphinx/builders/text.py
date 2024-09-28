"""Plain-text Sphinx builder."""
from __future__ import annotations
from os import path
from typing import TYPE_CHECKING
from docutils.io import StringOutput
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.osutil import _last_modified_time, ensuredir, os_path
from sphinx.writers.text import TextTranslator, TextWriter
if TYPE_CHECKING:
    from collections.abc import Iterator
    from docutils import nodes
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class TextBuilder(Builder):
    name = 'text'
    format = 'text'
    epilog = __('The text files are in %(outdir)s.')
    out_suffix = '.txt'
    allow_parallel = True
    default_translator_class = TextTranslator
    current_docname: str | None = None