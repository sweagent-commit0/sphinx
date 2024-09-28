"""Transforms for HTML builder."""
from __future__ import annotations
import re
from typing import TYPE_CHECKING, Any
from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.nodes import NodeMatcher
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

class KeyboardTransform(SphinxPostTransform):
    """Transform :kbd: role to more detailed form.

    Before::

        <literal class="kbd">
            Control-x

    After::

        <literal class="kbd compound">
            <literal class="kbd">
                Control
            -
            <literal class="kbd">
                x
    """
    default_priority = 400
    formats = ('html',)
    pattern = re.compile('(?<=.)(-|\\+|\\^|\\s+)(?=.)')
    multiwords_keys = (('caps', 'lock'), ('page', 'down'), ('page', 'up'), ('scroll', 'lock'), ('num', 'lock'), ('sys', 'rq'), ('back', 'space'))