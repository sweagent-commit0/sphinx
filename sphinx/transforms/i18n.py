"""Docutils transforms used by Sphinx when reading documents."""
from __future__ import annotations
import contextlib
from os import path
from re import DOTALL, match
from textwrap import indent
from typing import TYPE_CHECKING, Any, TypeVar
from docutils import nodes
from docutils.io import StringInput
from sphinx import addnodes
from sphinx.domains.std import make_glossary_term, split_term_classifiers
from sphinx.errors import ConfigError
from sphinx.locale import __
from sphinx.locale import init as init_locale
from sphinx.transforms import SphinxTransform
from sphinx.util import get_filetype, logging
from sphinx.util.i18n import docname_to_domain
from sphinx.util.index_entries import split_index_msg
from sphinx.util.nodes import IMAGE_TYPE_NODES, LITERAL_TYPE_NODES, NodeMatcher, extract_messages, traverse_translatable_index
if TYPE_CHECKING:
    from collections.abc import Sequence
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)
EXCLUDED_PENDING_XREF_ATTRIBUTES = ('refexplicit',)
N = TypeVar('N', bound=nodes.Node)

def publish_msgstr(app: Sphinx, source: str, source_path: str, source_line: int, config: Config, settings: Any) -> nodes.Element:
    """Publish msgstr (single line) into docutils document

    :param sphinx.application.Sphinx app: sphinx application
    :param str source: source text
    :param str source_path: source path for warning indication
    :param source_line: source line for warning indication
    :param sphinx.config.Config config: sphinx config
    :param docutils.frontend.Values settings: docutils settings
    :return: document
    :rtype: docutils.nodes.document
    """
    pass

class PreserveTranslatableMessages(SphinxTransform):
    """
    Preserve original translatable messages before translation
    """
    default_priority = 10

class _NodeUpdater:
    """Contains logic for updating one node with the translated content."""

    def __init__(self, node: nodes.Element, patch: nodes.Element, document: nodes.document, noqa: bool) -> None:
        self.node: nodes.Element = node
        self.patch: nodes.Element = patch
        self.document: nodes.document = document
        self.noqa: bool = noqa

    def compare_references(self, old_refs: Sequence[nodes.Element], new_refs: Sequence[nodes.Element], warning_msg: str) -> None:
        """Warn about mismatches between references in original and translated content."""
        pass

class Locale(SphinxTransform):
    """
    Replace translatable nodes with their translated doctree.
    """
    default_priority = 20

class TranslationProgressTotaliser(SphinxTransform):
    """
    Calculate the number of translated and untranslated nodes.
    """
    default_priority = 25

class AddTranslationClasses(SphinxTransform):
    """
    Add ``translated`` or ``untranslated`` classes to indicate translation status.
    """
    default_priority = 950

class RemoveTranslatableInline(SphinxTransform):
    """
    Remove inline nodes used for translation as placeholders.
    """
    default_priority = 999