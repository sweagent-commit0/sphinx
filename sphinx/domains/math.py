"""The math domain."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from docutils import nodes
from docutils.nodes import Element, Node, make_id, system_message
from sphinx.domains import Domain
from sphinx.locale import __
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.nodes import make_refnode
if TYPE_CHECKING:
    from collections.abc import Iterable
    from sphinx.addnodes import pending_xref
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class MathReferenceRole(XRefRole):
    pass

class MathDomain(Domain):
    """Mathematics domain."""
    name = 'math'
    label = 'mathematics'
    initial_data: dict[str, Any] = {'objects': {}, 'has_equations': {}}
    dangling_warnings = {'eq': 'equation not found: %(target)s'}
    enumerable_nodes = {nodes.math_block: ('displaymath', None)}
    roles = {'numref': MathReferenceRole()}