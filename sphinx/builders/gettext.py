"""The MessageCatalogBuilder class."""
from __future__ import annotations
import operator
import time
from codecs import open
from collections import defaultdict
from os import getenv, path, walk
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal
from uuid import uuid4
from docutils import nodes
from sphinx import addnodes, package_dir
from sphinx.builders import Builder
from sphinx.errors import ThemeError
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.console import bold
from sphinx.util.display import status_iterator
from sphinx.util.i18n import CatalogInfo, docname_to_domain
from sphinx.util.index_entries import split_index_msg
from sphinx.util.nodes import extract_messages, traverse_translatable_index
from sphinx.util.osutil import canon_path, ensuredir, relpath
from sphinx.util.tags import Tags
from sphinx.util.template import SphinxRenderer
if TYPE_CHECKING:
    import os
    from collections.abc import Iterable, Iterator, Sequence
    from docutils.nodes import Element
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util.typing import ExtensionMetadata
DEFAULT_TEMPLATE_PATH = Path(package_dir, 'templates', 'gettext')
logger = logging.getLogger(__name__)

class Message:
    """An entry of translatable message."""

    def __init__(self, text: str, locations: list[tuple[str, int]], uuids: list[str]) -> None:
        self.text = text
        self.locations = locations
        self.uuids = uuids

class Catalog:
    """Catalog of translatable messages."""

    def __init__(self) -> None:
        self.messages: list[str] = []
        self.metadata: dict[str, list[tuple[str, int, str]]] = {}

    def __iter__(self) -> Iterator[Message]:
        for message in self.messages:
            positions = sorted({(source, line) for source, line, uuid in self.metadata[message]})
            uuids = [uuid for source, line, uuid in self.metadata[message]]
            yield Message(message, positions, uuids)

class MsgOrigin:
    """
    Origin holder for Catalog message origin.
    """

    def __init__(self, source: str, line: int) -> None:
        self.source = source
        self.line = line
        self.uid = uuid4().hex

class GettextRenderer(SphinxRenderer):

    def __init__(self, template_path: Sequence[str | os.PathLike[str]] | None=None, outdir: str | os.PathLike[str] | None=None) -> None:
        self.outdir = outdir
        if template_path is None:
            super().__init__([DEFAULT_TEMPLATE_PATH])
        else:
            super().__init__([*template_path, DEFAULT_TEMPLATE_PATH])

        def escape(s: str) -> str:
            s = s.replace('\\', '\\\\')
            s = s.replace('"', '\\"')
            return s.replace('\n', '\\n"\n"')
        self.env.filters['e'] = escape
        self.env.filters['escape'] = escape

class I18nTags(Tags):
    """Dummy tags module for I18nBuilder.

    To ensure that all text inside ``only`` nodes is translated,
    this class always returns ``True`` regardless the defined tags.
    """

class I18nBuilder(Builder):
    """
    General i18n builder.
    """
    name = 'i18n'
    versioning_method = 'text'
    use_message_catalog = False
if (source_date_epoch := getenv('SOURCE_DATE_EPOCH')) is not None:
    timestamp = time.gmtime(float(source_date_epoch))
else:
    timestamp = time.localtime()
ctime = time.strftime('%Y-%m-%d %H:%M%z', timestamp)

def _is_node_in_substitution_definition(node: nodes.Node) -> bool:
    """Check "node" to test if it is in a substitution definition."""
    pass

class MessageCatalogBuilder(I18nBuilder):
    """
    Builds gettext-style message catalogs (.pot files).
    """
    name = 'gettext'
    epilog = __('The message catalogs are in %(outdir)s.')