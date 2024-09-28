"""docutils writers handling Sphinx' custom nodes."""
from __future__ import annotations
from typing import TYPE_CHECKING, cast
from docutils.writers.html4css1 import Writer
from sphinx.util import logging
from sphinx.writers.html5 import HTML5Translator
if TYPE_CHECKING:
    from sphinx.builders.html import StandaloneHTMLBuilder
logger = logging.getLogger(__name__)
HTMLTranslator = HTML5Translator

class HTMLWriter(Writer):
    settings_default_overrides = {'embed_stylesheet': False}

    def __init__(self, builder: StandaloneHTMLBuilder) -> None:
        super().__init__()
        self.builder = builder