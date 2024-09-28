"""Utility function and classes for Sphinx projects."""
from __future__ import annotations
import contextlib
import os
from pathlib import Path
from typing import TYPE_CHECKING
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util._pathlib import _StrPath
from sphinx.util.matching import get_matching_files
from sphinx.util.osutil import path_stabilize
if TYPE_CHECKING:
    from collections.abc import Iterable
logger = logging.getLogger(__name__)
EXCLUDE_PATHS = ['**/_sources', '.#*', '**/.#*', '*.lproj/**']

class Project:
    """A project is the source code set of the Sphinx document(s)."""

    def __init__(self, srcdir: str | os.PathLike[str], source_suffix: Iterable[str]) -> None:
        self.srcdir = _StrPath(srcdir)
        self.source_suffix = tuple(source_suffix)
        self._first_source_suffix = next(iter(self.source_suffix), '')
        self.docnames: set[str] = set()
        self._path_to_docname: dict[Path, str] = {}
        self._docname_to_path: dict[str, Path] = {}

    def restore(self, other: Project) -> None:
        """Take over a result of last build."""
        pass

    def discover(self, exclude_paths: Iterable[str]=(), include_paths: Iterable[str]=('**',)) -> set[str]:
        """Find all document files in the source directory and put them in
        :attr:`docnames`.
        """
        pass

    def path2doc(self, filename: str | os.PathLike[str]) -> str | None:
        """Return the docname for the filename if the file is a document.

        *filename* should be absolute or relative to the source directory.
        """
        pass

    def doc2path(self, docname: str, absolute: bool) -> _StrPath:
        """Return the filename for the document name.

        If *absolute* is True, return as an absolute path.
        Else, return as a relative path to the source directory.
        """
        pass