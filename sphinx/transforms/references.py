"""Docutils transforms used by Sphinx."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from docutils.transforms.references import DanglingReferences
from sphinx.transforms import SphinxTransform
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

class SphinxDanglingReferences(DanglingReferences):
    """DanglingReferences transform which does not output info messages."""

class SphinxDomains(SphinxTransform):
    """Collect objects to Sphinx domains for cross references."""
    default_priority = 850