from __future__ import annotations
import hashlib
import os.path
from typing import Any

class FilenameUniqDict(dict[str, tuple[set[str], str]]):
    """
    A dictionary that automatically generates unique names for its keys,
    interpreted as filenames, and keeps track of a set of docnames they
    appear in.  Used for images and downloadable files in the environment.
    """

    def __init__(self) -> None:
        self._existing: set[str] = set()

    def __getstate__(self) -> set[str]:
        return self._existing

    def __setstate__(self, state: set[str]) -> None:
        self._existing = state

class DownloadFiles(dict[str, tuple[set[str], str]]):
    """A special dictionary for download files.

    .. important:: This class would be refactored in nearly future.
                   Hence don't hack this directly.
    """