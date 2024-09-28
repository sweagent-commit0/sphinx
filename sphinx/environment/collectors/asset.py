"""The image collector for sphinx.environment."""
from __future__ import annotations
import os
from glob import glob
from os import path
from typing import TYPE_CHECKING
from docutils import nodes
from docutils.utils import relative_path
from sphinx import addnodes
from sphinx.environment.collectors import EnvironmentCollector
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.i18n import get_image_filename_for_language, search_image_for_language
from sphinx.util.images import guess_mimetype
if TYPE_CHECKING:
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class ImageCollector(EnvironmentCollector):
    """Image files collector for sphinx.environment."""

    def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
        """Process and rewrite image URIs."""
        pass

class DownloadFileCollector(EnvironmentCollector):
    """Download files collector for sphinx.environment."""

    def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
        """Process downloadable file paths."""
        pass