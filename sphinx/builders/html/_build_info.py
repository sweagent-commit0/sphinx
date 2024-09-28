"""Record metadata for the build process."""
from __future__ import annotations
import hashlib
import types
from typing import TYPE_CHECKING
from sphinx.locale import __
if TYPE_CHECKING:
    from collections.abc import Set
    from pathlib import Path
    from typing import Any
    from sphinx.config import Config, _ConfigRebuild
    from sphinx.util.tags import Tags

class BuildInfo:
    """buildinfo file manipulator.

    HTMLBuilder and its family are storing their own envdata to ``.buildinfo``.
    This class is a manipulator for the file.
    """

    def __init__(self, config: Config | None=None, tags: Tags | None=None, config_categories: Set[_ConfigRebuild]=frozenset()) -> None:
        self.config_hash = ''
        self.tags_hash = ''
        if config:
            values = {c.name: c.value for c in config.filter(config_categories)}
            self.config_hash = _stable_hash(values)
        if tags:
            self.tags_hash = _stable_hash(sorted(tags))

    def __eq__(self, other: BuildInfo) -> bool:
        return self.config_hash == other.config_hash and self.tags_hash == other.tags_hash

def _stable_hash(obj: Any) -> str:
    """Return a stable hash for a Python data structure.

    We can't just use the md5 of str(obj) as the order of collections
    may be random.
    """
    pass