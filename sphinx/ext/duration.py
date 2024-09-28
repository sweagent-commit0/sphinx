"""Measure document reading durations."""
from __future__ import annotations
import time
from itertools import islice
from operator import itemgetter
from typing import TYPE_CHECKING, cast
import sphinx
from sphinx.domains import Domain
from sphinx.locale import __
from sphinx.util import logging
if TYPE_CHECKING:
    from typing import TypedDict
    from docutils import nodes
    from sphinx.application import Sphinx

    class _DurationDomainData(TypedDict):
        reading_durations: dict[str, float]
logger = logging.getLogger(__name__)

class DurationDomain(Domain):
    """A domain for durations of Sphinx processing."""
    name = 'duration'

def on_builder_inited(app: Sphinx) -> None:
    """Initialize DurationDomain on bootstrap.

    This clears the results of the last build.
    """
    pass

def on_source_read(app: Sphinx, docname: str, content: list[str]) -> None:
    """Start to measure reading duration."""
    pass

def on_doctree_read(app: Sphinx, doctree: nodes.document) -> None:
    """Record a reading duration."""
    pass

def on_build_finished(app: Sphinx, error: Exception) -> None:
    """Display duration ranking on the current build."""
    pass