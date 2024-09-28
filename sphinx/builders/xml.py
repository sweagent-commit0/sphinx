"""Docutils-native XML and pseudo-XML builders."""
from __future__ import annotations
from os import path
from typing import TYPE_CHECKING
from docutils import nodes
from docutils.io import StringOutput
from docutils.writers.docutils_xml import XMLTranslator
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.osutil import _last_modified_time, ensuredir, os_path
from sphinx.writers.xml import PseudoXMLWriter, XMLWriter
if TYPE_CHECKING:
    from collections.abc import Iterator
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class XMLBuilder(Builder):
    """
    Builds Docutils-native XML.
    """
    name = 'xml'
    format = 'xml'
    epilog = __('The XML files are in %(outdir)s.')
    out_suffix = '.xml'
    allow_parallel = True
    _writer_class: type[XMLWriter] | type[PseudoXMLWriter] = XMLWriter
    writer: XMLWriter | PseudoXMLWriter
    default_translator_class = XMLTranslator

class PseudoXMLBuilder(XMLBuilder):
    """
    Builds pseudo-XML for display purposes.
    """
    name = 'pseudoxml'
    format = 'pseudoxml'
    epilog = __('The pseudo-XML files are in %(outdir)s.')
    out_suffix = '.pseudoxml'
    _writer_class = PseudoXMLWriter