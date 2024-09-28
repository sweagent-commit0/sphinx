"""Do syntax checks, but no writing."""
from __future__ import annotations
from typing import TYPE_CHECKING
from sphinx.builders import Builder
from sphinx.locale import __
if TYPE_CHECKING:
    from docutils import nodes
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

class DummyBuilder(Builder):
    name = 'dummy'
    epilog = __('The dummy builder generates no files.')
    allow_parallel = True