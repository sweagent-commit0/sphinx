"""A Base class for additional parsers."""
from __future__ import annotations
from typing import TYPE_CHECKING
import docutils.parsers
import docutils.parsers.rst
from docutils import nodes
from docutils.parsers.rst import states
from docutils.statemachine import StringList
from docutils.transforms.universal import SmartQuotes
from sphinx.util.rst import append_epilog, prepend_prolog
if TYPE_CHECKING:
    from docutils.transforms import Transform
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata

class Parser(docutils.parsers.Parser):
    """
    A base class of source parsers.  The additional parsers should inherit this class instead
    of ``docutils.parsers.Parser``.  Compared with ``docutils.parsers.Parser``, this class
    improves accessibility to Sphinx APIs.

    The subclasses can access sphinx core runtime objects (app, config and env).
    """
    config: Config
    env: BuildEnvironment

    def set_application(self, app: Sphinx) -> None:
        """set_application will be called from Sphinx to set app and other instance variables

        :param sphinx.application.Sphinx app: Sphinx application object
        """
        pass

class RSTParser(docutils.parsers.rst.Parser, Parser):
    """A reST parser for Sphinx."""

    def get_transforms(self) -> list[type[Transform]]:
        """
        Sphinx's reST parser replaces a transform class for smart-quotes by its own

        refs: sphinx.io.SphinxStandaloneReader
        """
        pass

    def parse(self, inputstring: str | StringList, document: nodes.document) -> None:
        """Parse text and generate a document tree."""
        pass

    def decorate(self, content: StringList) -> None:
        """Preprocess reST content before parsing."""
        pass