"""Base class of epub2/epub3 builders."""
from __future__ import annotations
import html
import os
import re
import time
from os import path
from typing import TYPE_CHECKING, Any, NamedTuple
from urllib.parse import quote
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile
from docutils import nodes
from docutils.utils import smartquotes
from sphinx import addnodes
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.builders.html._build_info import BuildInfo
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.display import status_iterator
from sphinx.util.fileutil import copy_asset_file
from sphinx.util.osutil import copyfile, ensuredir, relpath
if TYPE_CHECKING:
    from docutils.nodes import Element, Node
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
logger = logging.getLogger(__name__)
COVERPAGE_NAME = 'epub-cover.xhtml'
TOCTREE_TEMPLATE = 'toctree-l%d'
LINK_TARGET_TEMPLATE = ' [%(uri)s]'
FOOTNOTE_LABEL_TEMPLATE = '#%d'
FOOTNOTES_RUBRIC_NAME = 'Footnotes'
CSS_LINK_TARGET_CLASS = 'link-target'
GUIDE_TITLES = {'toc': 'Table of Contents', 'cover': 'Cover'}
MEDIA_TYPES = {'.xhtml': 'application/xhtml+xml', '.css': 'text/css', '.png': 'image/png', '.webp': 'image/webp', '.gif': 'image/gif', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.otf': 'font/otf', '.ttf': 'font/ttf', '.woff': 'font/woff'}
VECTOR_GRAPHICS_EXTENSIONS = ('.svg',)
REFURI_RE = re.compile('([^#:]*#)(.*)')

class ManifestItem(NamedTuple):
    href: str
    id: str
    media_type: str

class Spine(NamedTuple):
    idref: str
    linear: bool

class Guide(NamedTuple):
    type: str
    title: str
    uri: str

class NavPoint(NamedTuple):
    navpoint: str
    playorder: int
    text: str
    refuri: str
    children: list[NavPoint]
ssp = sphinx_smarty_pants

class EpubBuilder(StandaloneHTMLBuilder):
    """
    Builder that outputs epub files.

    It creates the metainfo files container.opf, toc.ncx, mimetype, and
    META-INF/container.xml.  Afterwards, all necessary files are zipped to an
    epub file.
    """
    copysource = False
    supported_image_types = ['image/svg+xml', 'image/png', 'image/gif', 'image/jpeg']
    supported_remote_images = False
    add_permalinks = False
    allow_sharp_as_current_path = False
    embedded = True
    download_support = False
    html_scaled_image_link = False
    search = False
    coverpage_name = COVERPAGE_NAME
    toctree_template = TOCTREE_TEMPLATE
    link_target_template = LINK_TARGET_TEMPLATE
    css_link_target_class = CSS_LINK_TARGET_CLASS
    guide_titles = GUIDE_TITLES
    media_types = MEDIA_TYPES
    refuri_re = REFURI_RE
    template_dir = ''
    doctype = ''

    def make_id(self, name: str) -> str:
        """Return a unique id for name."""
        pass

    def get_refnodes(self, doctree: Node, result: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Collect section titles, their depth in the toc and the refuri."""
        pass

    def get_toc(self) -> None:
        """Get the total table of contents, containing the root_doc
        and pre and post files not managed by sphinx.
        """
        pass

    def toc_add_files(self, refnodes: list[dict[str, Any]]) -> None:
        """Add the root_doc, pre and post files to a list of refnodes.
        """
        pass

    def fix_fragment(self, prefix: str, fragment: str) -> str:
        """Return a href/id attribute with colons replaced by hyphens."""
        pass

    def fix_ids(self, tree: nodes.document) -> None:
        """Replace colons with hyphens in href and id attributes.

        Some readers crash because they interpret the part as a
        transport protocol specification.
        """
        pass

    def add_visible_links(self, tree: nodes.document, show_urls: str='inline') -> None:
        """Add visible link targets for external links"""
        pass

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        """Write one document file.

        This method is overwritten in order to fix fragment identifiers
        and to add visible external links.
        """
        pass

    def fix_genindex(self, tree: list[tuple[str, list[tuple[str, Any]]]]) -> None:
        """Fix href attributes for genindex pages."""
        pass

    def is_vector_graphics(self, filename: str) -> bool:
        """Does the filename extension indicate a vector graphic format?"""
        pass

    def copy_image_files_pil(self) -> None:
        """Copy images using Pillow, the Python Imaging Library.
        The method tries to read and write the files with Pillow, converting
        the format and resizing the image if necessary/possible.
        """
        pass

    def copy_image_files(self) -> None:
        """Copy image files to destination directory.
        This overwritten method can use Pillow to convert image files.
        """
        pass

    def handle_page(self, pagename: str, addctx: dict[str, Any], templatename: str='page.html', outfilename: str | None=None, event_arg: Any=None) -> None:
        """Create a rendered page.

        This method is overwritten for genindex pages in order to fix href link
        attributes.
        """
        pass

    def build_mimetype(self) -> None:
        """Write the metainfo file mimetype."""
        pass

    def build_container(self, outname: str='META-INF/container.xml') -> None:
        """Write the metainfo file META-INF/container.xml."""
        pass

    def content_metadata(self) -> dict[str, Any]:
        """Create a dictionary with all metadata for the content.opf
        file properly escaped.
        """
        pass

    def build_content(self) -> None:
        """Write the metainfo file content.opf It contains bibliographic data,
        a file list and the spine (the reading order).
        """
        pass

    def new_navpoint(self, node: dict[str, Any], level: int, incr: bool=True) -> NavPoint:
        """Create a new entry in the toc from the node at given level."""
        pass

    def build_navpoints(self, nodes: list[dict[str, Any]]) -> list[NavPoint]:
        """Create the toc navigation structure.

        Subelements of a node are nested inside the navpoint.  For nested nodes
        the parent node is reinserted in the subnav.
        """
        pass

    def toc_metadata(self, level: int, navpoints: list[NavPoint]) -> dict[str, Any]:
        """Create a dictionary with all metadata for the toc.ncx file
        properly escaped.
        """
        pass

    def build_toc(self) -> None:
        """Write the metainfo file toc.ncx."""
        pass

    def build_epub(self) -> None:
        """Write the epub file.

        It is a zip file with the mimetype file stored uncompressed as the first
        entry.
        """
        pass