"""Changelog builder."""
from __future__ import annotations
import html
from os import path
from typing import TYPE_CHECKING, Any, cast
from sphinx import package_dir
from sphinx.builders import Builder
from sphinx.domains.changeset import ChangeSetDomain
from sphinx.locale import _, __
from sphinx.theming import HTMLThemeFactory
from sphinx.util import logging
from sphinx.util.console import bold
from sphinx.util.fileutil import copy_asset_file
from sphinx.util.osutil import ensuredir, os_path
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class ChangesBuilder(Builder):
    """
    Write a summary with all versionadded/changed/deprecated/removed directives.
    """
    name = 'changes'
    epilog = __('The overview file is in %(outdir)s.')
    typemap = {'versionadded': 'added', 'versionchanged': 'changed', 'deprecated': 'deprecated', 'versionremoved': 'removed'}