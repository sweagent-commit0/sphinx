"""Utilities for Sphinx extensions."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from packaging.version import InvalidVersion, Version
from sphinx.errors import VersionRequirementError
from sphinx.locale import __
from sphinx.util import logging
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class Extension:

    def __init__(self, name: str, module: Any, **kwargs: Any) -> None:
        self.name = name
        self.module = module
        self.metadata: ExtensionMetadata = kwargs
        self.version = kwargs.pop('version', 'unknown version')
        self.parallel_read_safe = kwargs.pop('parallel_read_safe', None)
        self.parallel_write_safe = kwargs.pop('parallel_write_safe', True)

def verify_needs_extensions(app: Sphinx, config: Config) -> None:
    """Check that extensions mentioned in :confval:`needs_extensions` satisfy the version
    requirement, and warn if an extension is not loaded.

    Warns if an extension in :confval:`needs_extension` is not loaded.

    :raises VersionRequirementError: if the version of an extension in
    :confval:`needs_extension` is unknown or older than the required version.
    """
    pass