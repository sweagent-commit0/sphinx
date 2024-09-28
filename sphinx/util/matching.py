"""Pattern-matching utility functions for Sphinx."""
from __future__ import annotations
import os.path
import re
from typing import TYPE_CHECKING
from sphinx.util.osutil import canon_path, path_stabilize
if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator

def _translate_pattern(pat: str) -> str:
    """Translate a shell-style glob pattern to a regular expression.

    Adapted from the fnmatch module, but enhanced so that single stars don't
    match slashes.
    """
    pass

class Matcher:
    """A pattern matcher for Multiple shell-style glob patterns.

    Note: this modifies the patterns to work with copy_asset().
          For example, "**/index.rst" matches with "index.rst"
    """

    def __init__(self, exclude_patterns: Iterable[str]) -> None:
        expanded = [pat[3:] for pat in exclude_patterns if pat.startswith('**/')]
        self.patterns = compile_matchers(list(exclude_patterns) + expanded)

    def __call__(self, string: str) -> bool:
        return self.match(string)
DOTFILES = Matcher(['**/.*'])
_pat_cache: dict[str, re.Pattern[str]] = {}

def patmatch(name: str, pat: str) -> re.Match[str] | None:
    """Return if name matches the regular expression (pattern)
    ``pat```. Adapted from fnmatch module.
    """
    pass

def patfilter(names: Iterable[str], pat: str) -> list[str]:
    """Return the subset of the list ``names`` that match
    the regular expression (pattern) ``pat``.

    Adapted from fnmatch module.
    """
    pass

def get_matching_files(dirname: str | os.PathLike[str], include_patterns: Iterable[str]=('**',), exclude_patterns: Iterable[str]=()) -> Iterator[str]:
    """Get all file names in a directory, recursively.

    Filter file names by the glob-style include_patterns and exclude_patterns.
    The default values include all files ("**") and exclude nothing ("").

    Only files matching some pattern in *include_patterns* are included, and
    exclusions from *exclude_patterns* take priority over inclusions.

    """
    pass