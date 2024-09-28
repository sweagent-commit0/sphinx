"""Directory HTML builders."""
from __future__ import annotations
from os import path
from typing import TYPE_CHECKING
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging
from sphinx.util.osutil import SEP, os_path
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class DirectoryHTMLBuilder(StandaloneHTMLBuilder):
    """
    A StandaloneHTMLBuilder that creates all HTML pages as "index.html" in
    a directory given by their pagename, so that generated URLs don't have
    ``.html`` in them.
    """
    name = 'dirhtml'