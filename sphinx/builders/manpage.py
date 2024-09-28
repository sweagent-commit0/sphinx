"""Manual pages builder."""
from __future__ import annotations
import warnings
from os import path
from typing import TYPE_CHECKING, Any
from docutils.frontend import OptionParser
from docutils.io import FileOutput
from sphinx import addnodes
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.console import darkgreen
from sphinx.util.display import progress_message
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.osutil import ensuredir, make_filename_from_project
from sphinx.writers.manpage import ManualPageTranslator, ManualPageWriter
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class ManualPageBuilder(Builder):
    """
    Builds groff output in manual page format.
    """
    name = 'man'
    format = 'man'
    epilog = __('The manual pages are in %(outdir)s.')
    default_translator_class = ManualPageTranslator
    supported_image_types: list[str] = []

def default_man_pages(config: Config) -> list[tuple[str, str, str, list[str], int]]:
    """Better default man_pages settings."""
    pass