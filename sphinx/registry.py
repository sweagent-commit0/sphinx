"""Sphinx component registry."""
from __future__ import annotations
import traceback
from importlib import import_module
from importlib.metadata import entry_points
from types import MethodType
from typing import TYPE_CHECKING, Any
from sphinx.domains import Domain, Index, ObjType
from sphinx.domains.std import GenericObject, Target
from sphinx.errors import ExtensionError, SphinxError, VersionRequirementError
from sphinx.extension import Extension
from sphinx.io import create_publisher
from sphinx.locale import __
from sphinx.parsers import Parser as SphinxParser
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.logging import prefixed_warnings
if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Sequence
    from docutils import nodes
    from docutils.core import Publisher
    from docutils.nodes import Element, Node, TextElement
    from docutils.parsers import Parser
    from docutils.parsers.rst import Directive
    from docutils.transforms import Transform
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.config import Config
    from sphinx.environment import BuildEnvironment
    from sphinx.ext.autodoc import Documenter
    from sphinx.util.typing import ExtensionMetadata, RoleFunction, TitleGetter, _ExtensionSetupFunc
logger = logging.getLogger(__name__)
EXTENSION_BLACKLIST = {'sphinxjp.themecore': '1.2', 'sphinxcontrib-napoleon': '1.3', 'sphinxprettysearchresults': '2.0.0'}

class SphinxComponentRegistry:

    def __init__(self) -> None:
        self.autodoc_attrgettrs: dict[type, Callable[[Any, str, Any], Any]] = {}
        self.builders: dict[str, type[Builder]] = {}
        self.documenters: dict[str, type[Documenter]] = {}
        self.css_files: list[tuple[str, dict[str, Any]]] = []
        self.domains: dict[str, type[Domain]] = {}
        self.domain_directives: dict[str, dict[str, type[Directive]]] = {}
        self.domain_indices: dict[str, list[type[Index]]] = {}
        self.domain_object_types: dict[str, dict[str, ObjType]] = {}
        self.domain_roles: dict[str, dict[str, RoleFunction | XRefRole]] = {}
        self.enumerable_nodes: dict[type[Node], tuple[str, TitleGetter | None]] = {}
        self.html_inline_math_renderers: dict[str, tuple[Callable, Callable | None]] = {}
        self.html_block_math_renderers: dict[str, tuple[Callable, Callable | None]] = {}
        self.html_assets_policy: str = 'per_page'
        self.html_themes: dict[str, str] = {}
        self.js_files: list[tuple[str | None, dict[str, Any]]] = []
        self.latex_packages: list[tuple[str, str | None]] = []
        self.latex_packages_after_hyperref: list[tuple[str, str | None]] = []
        self.post_transforms: list[type[Transform]] = []
        self.source_parsers: dict[str, type[Parser]] = {}
        self.source_suffix: dict[str, str] = {}
        self.translators: dict[str, type[nodes.NodeVisitor]] = {}
        self.translation_handlers: dict[str, dict[str, tuple[Callable, Callable | None]]] = {}
        self.transforms: list[type[Transform]] = []
        self.publishers: dict[str, Publisher] = {}

    def load_extension(self, app: Sphinx, extname: str) -> None:
        """Load a Sphinx extension."""
        pass

def merge_source_suffix(app: Sphinx, config: Config) -> None:
    """Merge any user-specified source_suffix with any added by extensions."""
    pass