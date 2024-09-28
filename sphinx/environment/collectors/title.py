"""The title collector components for sphinx.environment."""
from __future__ import annotations
from typing import TYPE_CHECKING
from docutils import nodes
from sphinx.environment.collectors import EnvironmentCollector
from sphinx.transforms import SphinxContentsFilter
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata

class TitleCollector(EnvironmentCollector):
    """title collector for sphinx.environment."""

    def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
        """Add a title node to the document (just copy the first section title),
        and store that title in the environment.
        """
        pass