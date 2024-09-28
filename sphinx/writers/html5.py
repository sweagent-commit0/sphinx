"""Experimental docutils writers for HTML5 handling Sphinx's custom nodes."""
from __future__ import annotations
import os
import posixpath
import re
import urllib.parse
from collections.abc import Iterable
from typing import TYPE_CHECKING, cast
from docutils import nodes
from docutils.writers.html5_polyglot import HTMLTranslator as BaseTranslator
from sphinx import addnodes
from sphinx.locale import _, __, admonitionlabels
from sphinx.util import logging
from sphinx.util.docutils import SphinxTranslator
from sphinx.util.images import get_image_size
if TYPE_CHECKING:
    from docutils.nodes import Element, Node, Text
    from sphinx.builders import Builder
    from sphinx.builders.html import StandaloneHTMLBuilder
logger = logging.getLogger(__name__)

def multiply_length(length: str, scale: int) -> str:
    """Multiply *length* (width or height) by *scale*."""
    pass

class HTML5Translator(SphinxTranslator, BaseTranslator):
    """
    Our custom HTML translator.
    """
    builder: StandaloneHTMLBuilder
    supported_inline_tags: set[str] = set()

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.highlighter = self.builder.highlighter
        self.docnames = [self.builder.current_docname]
        self.protect_literal_text = 0
        self.secnumber_suffix = self.config.html_secnumber_suffix
        self.param_separator = ''
        self.optional_param_level = 0
        self._table_row_indices = [0]
        self._fieldlist_row_indices = [0]
        self.required_params_left = 0

    def _visit_sig_parameter_list(self, node: Element, parameter_group: type[Element], sig_open_paren: str, sig_close_paren: str) -> None:
        """Visit a signature parameters or type parameters list.

        The *parameter_group* value is the type of child nodes acting as required parameters
        or as a set of contiguous optional parameters.
        """
        pass