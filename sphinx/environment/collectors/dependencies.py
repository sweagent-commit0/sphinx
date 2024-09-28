"""The dependencies collector components for sphinx.environment."""
from __future__ import annotations
import os
from os import path
from typing import TYPE_CHECKING
from docutils.utils import relative_path
from sphinx.environment.collectors import EnvironmentCollector
from sphinx.util.osutil import fs_encoding
if TYPE_CHECKING:
    from docutils import nodes
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata

class DependenciesCollector(EnvironmentCollector):
    """dependencies collector for sphinx.environment."""

    def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
        """Process docutils-generated dependency info."""
        pass