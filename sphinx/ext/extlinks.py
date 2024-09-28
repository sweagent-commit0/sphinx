"""Extension to save typing and prevent hard-coding of base URLs in reST files.

This adds a new config value called ``extlinks`` that is created like this::

   extlinks = {'exmpl': ('https://example.invalid/%s.html', caption), ...}

Now you can use e.g. :exmpl:`foo` in your documents.  This will create a
link to ``https://example.invalid/foo.html``.  The link caption depends on
the *caption* value given:

- If it is ``None``, the caption will be the full URL.
- If it is a string, it must contain ``%s`` exactly once.  In this case the
  caption will be *caption* with the role content substituted for ``%s``.

You can also give an explicit caption, e.g. :exmpl:`Foo <foo>`.

Both, the url string and the caption string must escape ``%`` as ``%%``.
"""
from __future__ import annotations
import re
from typing import TYPE_CHECKING, Any
from docutils import nodes, utils
import sphinx
from sphinx.locale import __
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import logging, rst
from sphinx.util.nodes import split_explicit_title
if TYPE_CHECKING:
    from collections.abc import Sequence
    from docutils.nodes import Node, system_message
    from docutils.parsers.rst.states import Inliner
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata, RoleFunction
logger = logging.getLogger(__name__)

class ExternalLinksChecker(SphinxPostTransform):
    """
    For each external link, check if it can be replaced by an extlink.

    We treat each ``reference`` node without ``internal`` attribute as an external link.
    """
    default_priority = 500

    def check_uri(self, refnode: nodes.reference) -> None:
        """
        If the URI in ``refnode`` has a replacement in ``extlinks``,
        emit a warning with a replacement suggestion.
        """
        pass