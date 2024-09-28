"""Manual page writer, extended for Sphinx custom nodes."""
from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, cast
from docutils import nodes
from docutils.writers.manpage import Translator as BaseTranslator
from docutils.writers.manpage import Writer
from sphinx import addnodes
from sphinx.locale import _, admonitionlabels
from sphinx.util import logging
from sphinx.util.docutils import SphinxTranslator
from sphinx.util.i18n import format_date
from sphinx.util.nodes import NodeMatcher
if TYPE_CHECKING:
    from docutils.nodes import Element
    from sphinx.builders import Builder
logger = logging.getLogger(__name__)

class ManualPageWriter(Writer):

    def __init__(self, builder: Builder) -> None:
        super().__init__()
        self.builder = builder

class NestedInlineTransform:
    """
    Flatten nested inline nodes:

    Before:
        <strong>foo=<emphasis>1</emphasis>
        &bar=<emphasis>2</emphasis></strong>
    After:
        <strong>foo=</strong><emphasis>var</emphasis>
        <strong>&bar=</strong><emphasis>2</emphasis>
    """

    def __init__(self, document: nodes.document) -> None:
        self.document = document

class ManualPageTranslator(SphinxTranslator, BaseTranslator):
    """
    Custom man page translator.
    """
    _docinfo: dict[str, Any] = {}

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.in_productionlist = 0
        self.section_level = -1
        self._docinfo['title'] = self.settings.title
        self._docinfo['subtitle'] = self.settings.subtitle
        if self.settings.authors:
            self._docinfo['author'] = self.settings.authors
        self._docinfo['manual_section'] = self.settings.section
        self._docinfo['title_upper'] = self._docinfo['title'].upper()
        if self.config.today:
            self._docinfo['date'] = self.config.today
        else:
            self._docinfo['date'] = format_date(self.config.today_fmt or _('%b %d, %Y'), language=self.config.language)
        self._docinfo['copyright'] = self.config.copyright
        self._docinfo['version'] = self.config.version
        self._docinfo['manual_group'] = self.config.project
        for label, translation in admonitionlabels.items():
            self.language.labels[label] = self.deunicode(translation)