"""Image converter extension for Sphinx"""
from __future__ import annotations
import subprocess
import sys
from subprocess import CalledProcessError
from typing import TYPE_CHECKING
import sphinx
from sphinx.errors import ExtensionError
from sphinx.locale import __
from sphinx.transforms.post_transforms.images import ImageConverter
from sphinx.util import logging
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class ImagemagickConverter(ImageConverter):
    conversion_rules = [('image/svg+xml', 'image/png'), ('image/gif', 'image/png'), ('application/pdf', 'image/png'), ('application/illustrator', 'image/png'), ('image/webp', 'image/png')]

    def is_available(self) -> bool:
        """Confirms the converter is available or not."""
        pass

    def convert(self, _from: str, _to: str) -> bool:
        """Converts the image to expected one."""
        pass