"""Docutils transforms used by Sphinx."""
from __future__ import annotations
import os
import re
from hashlib import sha1
from math import ceil
from pathlib import Path
from typing import TYPE_CHECKING, Any
from docutils import nodes
from sphinx.locale import __
from sphinx.transforms import SphinxTransform
from sphinx.util import logging, requests
from sphinx.util._pathlib import _StrPath
from sphinx.util.http_date import epoch_to_rfc1123, rfc1123_to_epoch
from sphinx.util.images import get_image_extension, guess_mimetype, parse_data_uri
from sphinx.util.osutil import ensuredir
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)
MAX_FILENAME_LEN = 32
CRITICAL_PATH_CHAR_RE = re.compile('[:;<>|*" ]')

class BaseImageConverter(SphinxTransform):
    pass

class ImageDownloader(BaseImageConverter):
    default_priority = 100

class DataURIExtractor(BaseImageConverter):
    default_priority = 150

class ImageConverter(BaseImageConverter):
    """A base class for image converters.

    An image converter is kind of Docutils transform module.  It is used to
    convert image files which are not supported by a builder to the
    appropriate format for that builder.

    For example, :py:class:`LaTeX builder <.LaTeXBuilder>` supports PDF,
    PNG and JPEG as image formats.  However it does not support SVG images.
    For such case, using image converters allows to embed these
    unsupported images into the document.  One of the image converters;
    :ref:`sphinx.ext.imgconverter <sphinx.ext.imgconverter>` can convert
    a SVG image to PNG format using Imagemagick internally.

    There are three steps to make your custom image converter:

    1. Make a subclass of ``ImageConverter`` class
    2. Override ``conversion_rules``, ``is_available()`` and ``convert()``
    3. Register your image converter to Sphinx using
       :py:meth:`.Sphinx.add_post_transform`
    """
    default_priority = 200
    available: bool | None = None
    conversion_rules: list[tuple[str, str]] = []

    def is_available(self) -> bool:
        """Return the image converter is available or not."""
        pass

    def convert(self, _from: str, _to: str) -> bool:
        """Convert an image file to the expected format.

        *_from* is a path of the source image file, and *_to* is a path
        of the destination file.
        """
        pass