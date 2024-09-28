"""To publish HTML docs at GitHub Pages, create .nojekyll file."""
from __future__ import annotations
import contextlib
import os
import urllib.parse
from typing import TYPE_CHECKING
import sphinx
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata

def _get_domain_from_url(url: str) -> str:
    """Get the domain from a URL."""
    pass

def create_nojekyll_and_cname(app: Sphinx, env: BuildEnvironment) -> None:
    """Manage the ``.nojekyll`` and ``CNAME`` files for GitHub Pages.

    For HTML-format builders (e.g. 'html', 'dirhtml') we unconditionally create
    the ``.nojekyll`` file to signal that GitHub Pages should not run Jekyll
    processing.

    If the :confval:`html_baseurl` option is set, we also create a CNAME file
    with the domain from ``html_baseurl``, so long as it is not a ``github.io``
    domain.

    If this extension is loaded and the domain in ``html_baseurl`` no longer
    requires a CNAME file, we remove any existing ``CNAME`` files from the
    output directory.
    """
    pass