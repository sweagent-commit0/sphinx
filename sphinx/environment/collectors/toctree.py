"""Toctree collector for sphinx.environment."""
from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar, cast
from docutils import nodes
from sphinx import addnodes
from sphinx.environment.adapters.toctree import note_toctree
from sphinx.environment.collectors import EnvironmentCollector
from sphinx.locale import __
from sphinx.transforms import SphinxContentsFilter
from sphinx.util import logging, url_re
if TYPE_CHECKING:
    from collections.abc import Sequence
    from docutils.nodes import Element, Node
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata
N = TypeVar('N')
logger = logging.getLogger(__name__)

class TocTreeCollector(EnvironmentCollector):

    def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
        """Build a TOC from the doctree and store it in the inventory."""
        pass

    def assign_section_numbers(self, env: BuildEnvironment) -> list[str]:
        """Assign a section number to each heading under a numbered toctree."""
        pass

    def assign_figure_numbers(self, env: BuildEnvironment) -> list[str]:
        """Assign a figure number to each figure under a numbered toctree."""
        pass