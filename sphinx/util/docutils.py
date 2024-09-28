"""Utility functions for docutils."""
from __future__ import annotations
import os
import re
from collections.abc import Sequence
from contextlib import contextmanager
from copy import copy
from os import path
from typing import IO, TYPE_CHECKING, Any, cast
import docutils
from docutils import nodes
from docutils.io import FileOutput
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.states import Inliner
from docutils.statemachine import State, StateMachine, StringList
from docutils.utils import Reporter, unescape
from sphinx.errors import SphinxError
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.parsing import nested_parse_to_nodes
logger = logging.getLogger(__name__)
report_re = re.compile('^(.+?:(?:\\d+)?): \\((DEBUG|INFO|WARNING|ERROR|SEVERE)/(\\d+)?\\) ')
if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from types import ModuleType
    from docutils.frontend import Values
    from docutils.nodes import Element, Node, system_message
    from sphinx.builders import Builder
    from sphinx.config import Config
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import RoleFunction
additional_nodes: set[type[Element]] = set()

@contextmanager
def docutils_namespace() -> Iterator[None]:
    """Create namespace for reST parsers."""
    pass

def is_directive_registered(name: str) -> bool:
    """Check the *name* directive is already registered."""
    pass

def register_directive(name: str, directive: type[Directive]) -> None:
    """Register a directive to docutils.

    This modifies global state of docutils.  So it is better to use this
    inside ``docutils_namespace()`` to prevent side-effects.
    """
    pass

def is_role_registered(name: str) -> bool:
    """Check the *name* role is already registered."""
    pass

def register_role(name: str, role: RoleFunction) -> None:
    """Register a role to docutils.

    This modifies global state of docutils.  So it is better to use this
    inside ``docutils_namespace()`` to prevent side-effects.
    """
    pass

def unregister_role(name: str) -> None:
    """Unregister a role from docutils."""
    pass

def is_node_registered(node: type[Element]) -> bool:
    """Check the *node* is already registered."""
    pass

def register_node(node: type[Element]) -> None:
    """Register a node to docutils.

    This modifies global state of some visitors.  So it is better to use this
    inside ``docutils_namespace()`` to prevent side-effects.
    """
    pass

def unregister_node(node: type[Element]) -> None:
    """Unregister a node from docutils.

    This is inverse of ``nodes._add_nodes_class_names()``.
    """
    pass

@contextmanager
def patched_get_language() -> Iterator[None]:
    """Patch docutils.languages.get_language() temporarily.

    This ignores the second argument ``reporter`` to suppress warnings.
    refs: https://github.com/sphinx-doc/sphinx/issues/3788
    """
    pass

@contextmanager
def patched_rst_get_language() -> Iterator[None]:
    """Patch docutils.parsers.rst.languages.get_language().
    Starting from docutils 0.17, get_language() in ``rst.languages``
    also has a reporter, which needs to be disabled temporarily.

    This should also work for old versions of docutils,
    because reporter is none by default.

    refs: https://github.com/sphinx-doc/sphinx/issues/10179
    """
    pass

@contextmanager
def using_user_docutils_conf(confdir: str | None) -> Iterator[None]:
    """Let docutils know the location of ``docutils.conf`` for Sphinx."""
    pass

@contextmanager
def patch_docutils(confdir: str | None=None) -> Iterator[None]:
    """Patch to docutils temporarily."""
    pass

class CustomReSTDispatcher:
    """Custom reST's mark-up dispatcher.

    This replaces docutils's directives and roles dispatch mechanism for reST parser
    by original one temporarily.
    """

    def __init__(self) -> None:
        self.directive_func: Callable = lambda *args: (None, [])
        self.roles_func: Callable = lambda *args: (None, [])

    def __enter__(self) -> None:
        self.enable()

    def __exit__(self, exc_type: type[Exception], exc_value: Exception, traceback: Any) -> None:
        self.disable()

class ElementLookupError(Exception):
    pass

class sphinx_domains(CustomReSTDispatcher):
    """Monkey-patch directive and role dispatch, so that domain-specific
    markup takes precedence.
    """

    def __init__(self, env: BuildEnvironment) -> None:
        self.env = env
        super().__init__()

    def lookup_domain_element(self, type: str, name: str) -> Any:
        """Lookup a markup element (directive or role), given its name which can
        be a full name (with domain).
        """
        pass

class WarningStream:
    pass

class LoggingReporter(Reporter):

    @classmethod
    def from_reporter(cls: type[LoggingReporter], reporter: Reporter) -> LoggingReporter:
        """Create an instance of LoggingReporter from other reporter object."""
        pass

    def __init__(self, source: str, report_level: int=Reporter.WARNING_LEVEL, halt_level: int=Reporter.SEVERE_LEVEL, debug: bool=False, error_handler: str='backslashreplace') -> None:
        stream = cast(IO, WarningStream())
        super().__init__(source, report_level, halt_level, stream, debug, error_handler=error_handler)

class NullReporter(Reporter):
    """A dummy reporter; write nothing."""

    def __init__(self) -> None:
        super().__init__('', 999, 4)

@contextmanager
def switch_source_input(state: State, content: StringList) -> Iterator[None]:
    """Switch current source input of state temporarily."""
    pass

class SphinxFileOutput(FileOutput):
    """Better FileOutput class for Sphinx."""

    def __init__(self, **kwargs: Any) -> None:
        self.overwrite_if_changed = kwargs.pop('overwrite_if_changed', False)
        kwargs.setdefault('encoding', 'utf-8')
        super().__init__(**kwargs)

class SphinxDirective(Directive):
    """A base class for Sphinx directives.

    This class provides helper methods for Sphinx directives.

    .. versionadded:: 1.8

    .. note:: The subclasses of this class might not work with docutils.
              This class is strongly coupled with Sphinx.
    """

    @property
    def env(self) -> BuildEnvironment:
        """Reference to the :class:`.BuildEnvironment` object.

        .. versionadded:: 1.8
        """
        pass

    @property
    def config(self) -> Config:
        """Reference to the :class:`.Config` object.

        .. versionadded:: 1.8
        """
        pass

    def get_source_info(self) -> tuple[str, int]:
        """Get source and line number.

        .. versionadded:: 3.0
        """
        pass

    def set_source_info(self, node: Node) -> None:
        """Set source and line number to the node.

        .. versionadded:: 2.1
        """
        pass

    def get_location(self) -> str:
        """Get current location info for logging.

        .. versionadded:: 4.2
        """
        pass

    def parse_content_to_nodes(self, allow_section_headings: bool=False) -> list[Node]:
        """Parse the directive's content into nodes.

        :param allow_section_headings:
            Are titles (sections) allowed in the directive's content?
            Note that this option bypasses Docutils' usual checks on
            doctree structure, and misuse of this option can lead to
            an incoherent doctree. In Docutils, section nodes should
            only be children of ``Structural`` nodes, which includes
            ``document``, ``section``, and ``sidebar`` nodes.

        .. versionadded:: 7.4
        """
        pass

    def parse_text_to_nodes(self, text: str='', /, *, offset: int=-1, allow_section_headings: bool=False) -> list[Node]:
        """Parse *text* into nodes.

        :param text:
            Text, in string form. ``StringList`` is also accepted.
        :param allow_section_headings:
            Are titles (sections) allowed in *text*?
            Note that this option bypasses Docutils' usual checks on
            doctree structure, and misuse of this option can lead to
            an incoherent doctree. In Docutils, section nodes should
            only be children of ``Structural`` nodes, which includes
            ``document``, ``section``, and ``sidebar`` nodes.
        :param offset:
            The offset of the content.

        .. versionadded:: 7.4
        """
        pass

    def parse_inline(self, text: str, *, lineno: int=-1) -> tuple[list[Node], list[system_message]]:
        """Parse *text* as inline elements.

        :param text:
            The text to parse, which should be a single line or paragraph.
            This cannot contain any structural elements (headings,
            transitions, directives, etc).
        :param lineno:
            The line number where the interpreted text begins.
        :returns:
            A list of nodes (text and inline elements) and a list of system_messages.

        .. versionadded:: 7.4
        """
        pass

class SphinxRole:
    """A base class for Sphinx roles.

    This class provides helper methods for Sphinx roles.

    .. versionadded:: 2.0

    .. note:: The subclasses of this class might not work with docutils.
              This class is strongly coupled with Sphinx.
    """
    name: str
    rawtext: str
    text: str
    lineno: int
    inliner: Inliner
    options: dict[str, Any]
    content: Sequence[str]

    def __call__(self, name: str, rawtext: str, text: str, lineno: int, inliner: Inliner, options: dict | None=None, content: Sequence[str]=()) -> tuple[list[Node], list[system_message]]:
        self.rawtext = rawtext
        self.text = unescape(text)
        self.lineno = lineno
        self.inliner = inliner
        self.options = options if options is not None else {}
        self.content = content
        if name:
            self.name = name.lower()
        else:
            self.name = self.env.temp_data.get('default_role', '')
            if not self.name:
                self.name = self.env.config.default_role
            if not self.name:
                msg = 'cannot determine default role!'
                raise SphinxError(msg)
        return self.run()

    @property
    def env(self) -> BuildEnvironment:
        """Reference to the :class:`.BuildEnvironment` object.

        .. versionadded:: 2.0
        """
        pass

    @property
    def config(self) -> Config:
        """Reference to the :class:`.Config` object.

        .. versionadded:: 2.0
        """
        pass

    def get_location(self) -> str:
        """Get current location info for logging.

        .. versionadded:: 4.2
        """
        pass

class ReferenceRole(SphinxRole):
    """A base class for reference roles.

    The reference roles can accept ``link title <target>`` style as a text for
    the role.  The parsed result; link title and target will be stored to
    ``self.title`` and ``self.target``.

    .. versionadded:: 2.0
    """
    has_explicit_title: bool
    disabled: bool
    title: str
    target: str
    explicit_title_re = re.compile('^(.+?)\\s*(?<!\\x00)<(.*?)>$', re.DOTALL)

    def __call__(self, name: str, rawtext: str, text: str, lineno: int, inliner: Inliner, options: dict | None=None, content: Sequence[str]=()) -> tuple[list[Node], list[system_message]]:
        if options is None:
            options = {}
        self.disabled = text.startswith('!')
        matched = self.explicit_title_re.match(text)
        if matched:
            self.has_explicit_title = True
            self.title = unescape(matched.group(1))
            self.target = unescape(matched.group(2))
        else:
            self.has_explicit_title = False
            self.title = unescape(text)
            self.target = unescape(text)
        return super().__call__(name, rawtext, text, lineno, inliner, options, content)

class SphinxTranslator(nodes.NodeVisitor):
    """A base class for Sphinx translators.

    This class adds a support for visitor/departure method for super node class
    if visitor/departure method for node class is not found.

    It also provides helper methods for Sphinx translators.

    .. versionadded:: 2.0

    .. note:: The subclasses of this class might not work with docutils.
              This class is strongly coupled with Sphinx.
    """

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document)
        self.builder = builder
        self.config = builder.config
        self.settings = document.settings

    def dispatch_visit(self, node: Node) -> None:
        """
        Dispatch node to appropriate visitor method.
        The priority of visitor method is:

        1. ``self.visit_{node_class}()``
        2. ``self.visit_{super_node_class}()``
        3. ``self.unknown_visit()``
        """
        pass

    def dispatch_departure(self, node: Node) -> None:
        """
        Dispatch node to appropriate departure method.
        The priority of departure method is:

        1. ``self.depart_{node_class}()``
        2. ``self.depart_{super_node_class}()``
        3. ``self.unknown_departure()``
        """
        pass
__document_cache__: tuple[Values, Reporter]

def new_document(source_path: str, settings: Any=None) -> nodes.document:
    """Return a new empty document object.  This is an alternative of docutils'.

    This is a simple wrapper for ``docutils.utils.new_document()``.  It
    caches the result of docutils' and use it on second call for instantiation.
    This makes an instantiation of document nodes much faster.
    """
    pass