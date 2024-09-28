"""Image utility functions for Sphinx."""
from __future__ import annotations
import base64
from os import path
from typing import TYPE_CHECKING, NamedTuple, overload
import imagesize
if TYPE_CHECKING:
    from os import PathLike
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
mime_suffixes = {'.gif': 'image/gif', '.jpg': 'image/jpeg', '.png': 'image/png', '.pdf': 'application/pdf', '.svg': 'image/svg+xml', '.svgz': 'image/svg+xml', '.ai': 'application/illustrator', '.webp': 'image/webp'}
_suffix_from_mime = {v: k for k, v in reversed(mime_suffixes.items())}

class DataURI(NamedTuple):
    mimetype: str
    charset: str
    data: bytes