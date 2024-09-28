"""Build epub3 files.

Originally derived from epub.py.
"""
from __future__ import annotations
import html
import os
import re
import time
from os import path
from typing import TYPE_CHECKING, Any, NamedTuple
from sphinx import package_dir
from sphinx.builders import _epub_base
from sphinx.config import ENUM, Config
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.fileutil import copy_asset_file
from sphinx.util.osutil import make_filename
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

class NavPoint(NamedTuple):
    text: str
    refuri: str
    children: list[NavPoint]
PAGE_PROGRESSION_DIRECTIONS = {'horizontal': 'ltr', 'vertical': 'rtl'}
IBOOK_SCROLL_AXIS = {'horizontal': 'vertical', 'vertical': 'horizontal'}
THEME_WRITING_MODES = {'vertical': 'vertical-rl', 'horizontal': 'horizontal-tb'}
DOCTYPE = '<!DOCTYPE html>'
HTML_TAG = '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">'
_xml_name_start_char = ':|[A-Z]|_|[a-z]|[À-Ö]|[Ø-ö]|[ø-˿]|[Ͱ-ͽ]|[Ϳ-\u1fff]|[\u200c-\u200d]|[⁰-\u218f]|[Ⰰ-\u2fef]|[、-\ud7ff]|[豈-﷏]|[ﷰ-�]|[𐀀-\U000effff]'
_xml_name_char = _xml_name_start_char + '\\-|\\.|[0-9]|·|[̀-ͯ]|[‿-⁀]'
_XML_NAME_PATTERN = re.compile(f'({_xml_name_start_char})({_xml_name_char})*')

class Epub3Builder(_epub_base.EpubBuilder):
    """
    Builder that outputs epub3 files.

    It creates the metainfo files content.opf, nav.xhtml, toc.ncx, mimetype,
    and META-INF/container.xml. Afterwards, all necessary files are zipped to
    an epub file.
    """
    name = 'epub'
    epilog = __('The ePub file is in %(outdir)s.')
    supported_remote_images = False
    template_dir = path.join(package_dir, 'templates', 'epub3')
    doctype = DOCTYPE
    html_tag = HTML_TAG
    use_meta_charset = True

    def handle_finish(self) -> None:
        """Create the metainfo files and finally the epub."""
        pass

    def content_metadata(self) -> dict[str, Any]:
        """Create a dictionary with all metadata for the content.opf
        file properly escaped.
        """
        pass

    def build_navlist(self, navnodes: list[dict[str, Any]]) -> list[NavPoint]:
        """Create the toc navigation structure.

        This method is almost same as build_navpoints method in epub.py.
        This is because the logical navigation structure of epub3 is not
        different from one of epub2.

        The difference from build_navpoints method is templates which are used
        when generating navigation documents.
        """
        pass

    def navigation_doc_metadata(self, navlist: list[NavPoint]) -> dict[str, Any]:
        """Create a dictionary with all metadata for the nav.xhtml file
        properly escaped.
        """
        pass

    def build_navigation_doc(self) -> None:
        """Write the metainfo file nav.xhtml."""
        pass

def convert_epub_css_files(app: Sphinx, config: Config) -> None:
    """Convert string styled epub_css_files to tuple styled one."""
    pass