"""Sphinx core events.

Gracefully adapted from the TextPress system by Armin.
"""
from __future__ import annotations
from collections import defaultdict
from operator import attrgetter
from typing import TYPE_CHECKING, NamedTuple, overload
from sphinx.errors import ExtensionError, SphinxError
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.inspect import safe_getattr
if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Sequence, Set
    from pathlib import Path
    from typing import Any, Literal
    from docutils import nodes
    from sphinx import addnodes
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.config import Config
    from sphinx.domains import Domain
    from sphinx.environment import BuildEnvironment
    from sphinx.ext.todo import todo_node
logger = logging.getLogger(__name__)

class EventListener(NamedTuple):
    id: int
    handler: Callable
    priority: int
core_events = {'config-inited': 'config', 'builder-inited': '', 'env-get-outdated': 'env, added, changed, removed', 'env-before-read-docs': 'env, docnames', 'env-purge-doc': 'env, docname', 'source-read': 'docname, source text', 'include-read': 'relative path, parent docname, source text', 'doctree-read': 'the doctree before being pickled', 'env-merge-info': 'env, read docnames, other env instance', 'env-updated': 'env', 'env-get-updated': 'env', 'env-check-consistency': 'env', 'write-started': 'builder', 'doctree-resolved': 'doctree, docname', 'missing-reference': 'env, node, contnode', 'warn-missing-reference': 'domain, node', 'build-finished': 'exception'}

class EventManager:
    """Event manager for Sphinx."""

    def __init__(self, app: Sphinx) -> None:
        self.app = app
        self.events = core_events.copy()
        self.listeners: dict[str, list[EventListener]] = defaultdict(list)
        self.next_listener_id = 0

    def add(self, name: str) -> None:
        """Register a custom Sphinx event."""
        pass

    def connect(self, name: str, callback: Callable, priority: int) -> int:
        """Connect a handler to specific event."""
        pass

    def disconnect(self, listener_id: int) -> None:
        """Disconnect a handler."""
        pass

    def emit(self, name: str, *args: Any, allowed_exceptions: tuple[type[Exception], ...]=()) -> list:
        """Emit a Sphinx event."""
        pass

    def emit_firstresult(self, name: str, *args: Any, allowed_exceptions: tuple[type[Exception], ...]=()) -> Any:
        """Emit a Sphinx event and returns first result.

        This returns the result of the first handler that doesn't return ``None``.
        """
        pass