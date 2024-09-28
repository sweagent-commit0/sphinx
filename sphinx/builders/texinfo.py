"""Texinfo builder."""
from __future__ import annotations
import os
import warnings
from os import path
from typing import TYPE_CHECKING, Any
from docutils import nodes
from docutils.frontend import OptionParser
from docutils.io import FileOutput
from sphinx import addnodes, package_dir
from sphinx.builders import Builder
from sphinx.environment.adapters.asset import ImageAdapter
from sphinx.errors import NoUri
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.console import darkgreen
from sphinx.util.display import progress_message, status_iterator
from sphinx.util.docutils import new_document
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.osutil import SEP, copyfile, ensuredir, make_filename_from_project
from sphinx.writers.texinfo import TexinfoTranslator, TexinfoWriter
if TYPE_CHECKING:
    from collections.abc import Iterable
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)
template_dir = os.path.join(package_dir, 'templates', 'texinfo')

class TexinfoBuilder(Builder):
    """
    Builds Texinfo output to create Info documentation.
    """
    name = 'texinfo'
    format = 'texinfo'
    epilog = __('The Texinfo files are in %(outdir)s.')
    if os.name == 'posix':
        epilog += __("\nRun 'make' in that directory to run these through makeinfo\n(use 'make info' here to do that automatically).")
    supported_image_types = ['image/png', 'image/jpeg', 'image/gif']
    default_translator_class = TexinfoTranslator

def default_texinfo_documents(config: Config) -> list[tuple[str, str, str, str, str, str, str]]:
    """Better default texinfo_documents settings."""
    pass