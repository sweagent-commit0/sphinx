"""Render math in HTML via dvipng or dvisvgm."""
from __future__ import annotations
__all__ = ()
import base64
import contextlib
import re
import shutil
import subprocess
import tempfile
from hashlib import sha1
from os import path
from subprocess import CalledProcessError
from typing import TYPE_CHECKING
from docutils import nodes
import sphinx
from sphinx import package_dir
from sphinx.errors import SphinxError
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.math import get_node_equation_number, wrap_displaymath
from sphinx.util.osutil import ensuredir
from sphinx.util.png import read_png_depth, write_png_depth
from sphinx.util.template import LaTeXRenderer
if TYPE_CHECKING:
    import os
    from docutils.nodes import Element
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.config import Config
    from sphinx.util.typing import ExtensionMetadata
    from sphinx.writers.html5 import HTML5Translator
logger = logging.getLogger(__name__)
templates_path = path.join(package_dir, 'templates', 'imgmath')

class MathExtError(SphinxError):
    category = 'Math extension error'

    def __init__(self, msg: str, stderr: str | None=None, stdout: str | None=None) -> None:
        if stderr:
            msg += '\n[stderr]\n' + stderr
        if stdout:
            msg += '\n[stdout]\n' + stdout
        super().__init__(msg)

class InvokeError(SphinxError):
    """errors on invoking converters."""
SUPPORT_FORMAT = ('png', 'svg')
depth_re = re.compile('\\[\\d+ depth=(-?\\d+)\\]')
depthsvg_re = re.compile('.*, depth=(.*)pt')
depthsvgcomment_re = re.compile('<!-- DEPTH=(-?\\d+) -->')

def read_svg_depth(filename: str) -> int | None:
    """Read the depth from comment at last line of SVG file
    """
    pass

def write_svg_depth(filename: str, depth: int) -> None:
    """Write the depth to SVG file as a comment at end of file
    """
    pass

def generate_latex_macro(image_format: str, math: str, config: Config, confdir: str | os.PathLike[str]='') -> str:
    """Generate LaTeX macro."""
    pass

def ensure_tempdir(builder: Builder) -> str:
    """Create temporary directory.

    use only one tempdir per build -- the use of a directory is cleaner
    than using temporary files, since we can clean up everything at once
    just removing the whole directory (see cleanup_tempdir)
    """
    pass

def compile_math(latex: str, builder: Builder) -> str:
    """Compile LaTeX macros for math to DVI."""
    pass

def convert_dvi_to_image(command: list[str], name: str) -> tuple[str, str]:
    """Convert DVI file to specific image format."""
    pass

def convert_dvi_to_png(dvipath: str, builder: Builder, out_path: str) -> int | None:
    """Convert DVI file to PNG image."""
    pass

def convert_dvi_to_svg(dvipath: str, builder: Builder, out_path: str) -> int | None:
    """Convert DVI file to SVG image."""
    pass

def render_math(self: HTML5Translator, math: str) -> tuple[str | None, int | None]:
    """Render the LaTeX math expression *math* using latex and dvipng or
    dvisvgm.

    Return the image absolute filename and the "depth",
    that is, the distance of image bottom and baseline in pixels, if the
    option to use preview_latex is switched on.

    Error handling may seem strange, but follows a pattern: if LaTeX or dvipng
    (dvisvgm) aren't available, only a warning is generated (since that enables
    people on machines without these programs to at least build the rest of the
    docs successfully).  If the programs are there, however, they may not fail
    since that indicates a problem in the math source.
    """
    pass