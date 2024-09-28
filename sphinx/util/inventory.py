"""Inventory utility functions for Sphinx."""
from __future__ import annotations
import os
import re
import zlib
from typing import IO, TYPE_CHECKING
from sphinx.locale import __
from sphinx.util import logging
BUFSIZE = 16 * 1024
logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import Inventory, InventoryItem

class InventoryFileReader:
    """A file reader for an inventory file.

    This reader supports mixture of texts and compressed texts.
    """

    def __init__(self, stream: IO[bytes]) -> None:
        self.stream = stream
        self.buffer = b''
        self.eof = False

class InventoryFile:
    pass