"""The changeset domain."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple, cast
from docutils import nodes
from sphinx import addnodes
from sphinx.domains import Domain
from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective
if TYPE_CHECKING:
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
versionlabels = {'versionadded': _('Added in version %s'), 'versionchanged': _('Changed in version %s'), 'deprecated': _('Deprecated since version %s'), 'versionremoved': _('Removed in version %s')}
versionlabel_classes = {'versionadded': 'added', 'versionchanged': 'changed', 'deprecated': 'deprecated', 'versionremoved': 'removed'}

class ChangeSet(NamedTuple):
    type: str
    docname: str
    lineno: int
    module: str | None
    descname: str | None
    content: str

class VersionChange(SphinxDirective):
    """
    Directive to describe a change/addition/deprecation in a specific version.
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec: ClassVar[OptionSpec] = {}

class ChangeSetDomain(Domain):
    """Domain for changesets."""
    name = 'changeset'
    label = 'changeset'
    initial_data: dict[str, dict[str, list[ChangeSet]]] = {'changes': {}}