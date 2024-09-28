"""The citation domain."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, cast
from docutils import nodes
from sphinx.addnodes import pending_xref
from sphinx.domains import Domain
from sphinx.locale import __
from sphinx.transforms import SphinxTransform
from sphinx.util import logging
from sphinx.util.nodes import copy_source_info, make_refnode
if TYPE_CHECKING:
    from docutils.nodes import Element
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class CitationDomain(Domain):
    """Domain for citations."""
    name = 'citation'
    label = 'citation'
    dangling_warnings = {'ref': 'citation not found: %(target)s'}

class CitationDefinitionTransform(SphinxTransform):
    """Mark citation definition labels as not smartquoted."""
    default_priority = 619

class CitationReferenceTransform(SphinxTransform):
    """
    Replace citation references by pending_xref nodes before the default
    docutils transform tries to resolve them.
    """
    default_priority = 619