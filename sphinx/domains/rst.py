"""The reStructuredText domain."""
from __future__ import annotations
import re
from typing import TYPE_CHECKING, Any, ClassVar, cast
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.locale import _, __
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.nodes import make_id, make_refnode
if TYPE_CHECKING:
    from collections.abc import Iterator
    from docutils.nodes import Element
    from sphinx.addnodes import desc_signature, pending_xref
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
logger = logging.getLogger(__name__)
dir_sig_re = re.compile('\\.\\. (.+?)::(.*)$')

class ReSTMarkup(ObjectDescription[str]):
    """
    Description of generic reST markup.
    """
    option_spec: ClassVar[OptionSpec] = {'no-index': directives.flag, 'no-index-entry': directives.flag, 'no-contents-entry': directives.flag, 'no-typesetting': directives.flag, 'noindex': directives.flag, 'noindexentry': directives.flag, 'nocontentsentry': directives.flag}

def parse_directive(d: str) -> tuple[str, str]:
    """Parse a directive signature.

    Returns (directive, arguments) string tuple.  If no arguments are given,
    returns (directive, '').
    """
    pass

class ReSTDirective(ReSTMarkup):
    """
    Description of a reST directive.
    """

class ReSTDirectiveOption(ReSTMarkup):
    """
    Description of an option for reST directive.
    """
    option_spec: ClassVar[OptionSpec] = ReSTMarkup.option_spec.copy()
    option_spec.update({'type': directives.unchanged})

class ReSTRole(ReSTMarkup):
    """
    Description of a reST role.
    """

class ReSTDomain(Domain):
    """ReStructuredText domain."""
    name = 'rst'
    label = 'reStructuredText'
    object_types = {'directive': ObjType(_('directive'), 'dir'), 'directive:option': ObjType(_('directive-option'), 'dir'), 'role': ObjType(_('role'), 'role')}
    directives = {'directive': ReSTDirective, 'directive:option': ReSTDirectiveOption, 'role': ReSTRole}
    roles = {'dir': XRefRole(), 'role': XRefRole()}
    initial_data: dict[str, dict[tuple[str, str], str]] = {'objects': {}}