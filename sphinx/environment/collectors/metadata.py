"""The metadata collector components for sphinx.environment."""
from __future__ import annotations
from typing import TYPE_CHECKING, cast
from docutils import nodes
from sphinx.environment.collectors import EnvironmentCollector
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata

class MetadataCollector(EnvironmentCollector):
    """metadata collector for sphinx.environment."""

    def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
        """Process the docinfo part of the doctree as metadata.

        Keep processing minimal -- just return what docutils says.
        """
        pass