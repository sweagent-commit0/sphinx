"""Add links to module code in Python object descriptions."""
from __future__ import annotations
import operator
import posixpath
import traceback
from importlib import import_module
from os import path
from typing import TYPE_CHECKING, Any, cast
from docutils import nodes
from docutils.nodes import Element, Node
import sphinx
from sphinx import addnodes
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.locale import _, __
from sphinx.pycode import ModuleAnalyzer
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import logging
from sphinx.util.display import status_iterator
from sphinx.util.nodes import make_refnode
from sphinx.util.osutil import _last_modified_time
if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)
OUTPUT_DIRNAME = '_modules'

class viewcode_anchor(Element):
    """Node for viewcode anchors.

    This node will be processed in the resolving phase.
    For viewcode supported builders, they will be all converted to the anchors.
    For not supported builders, they will be removed.
    """

class ViewcodeAnchorTransform(SphinxPostTransform):
    """Convert or remove viewcode_anchor nodes depends on builder."""
    default_priority = 100

def get_module_filename(app: Sphinx, modname: str) -> str | None:
    """Get module filename for *modname*."""
    pass

def should_generate_module_page(app: Sphinx, modname: str) -> bool:
    """Check generation of module page is needed."""
    pass