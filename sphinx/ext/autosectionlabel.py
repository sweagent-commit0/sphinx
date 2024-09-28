"""Allow reference sections by :ref: role using its title."""
from __future__ import annotations
from typing import TYPE_CHECKING, cast
from docutils import nodes
import sphinx
from sphinx.domains.std import StandardDomain
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.nodes import clean_astext
if TYPE_CHECKING:
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)