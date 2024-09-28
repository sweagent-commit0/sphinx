"""Defines a docutils directive for inserting inheritance diagrams.

Provide the directive with one or more classes or modules (separated
by whitespace).  For modules, all of the classes in that module will
be used.

Example::

   Given the following classes:

   class A: pass
   class B(A): pass
   class C(A): pass
   class D(B, C): pass
   class E(B): pass

   .. inheritance-diagram: D E

   Produces a graph like the following:

               A
              / \\
             B   C
            / \\ /
           E   D

The graph is inserted as a PNG+image map into HTML and a PDF in
LaTeX.
"""
from __future__ import annotations
import builtins
import hashlib
import inspect
import re
from collections.abc import Iterable, Sequence
from importlib import import_module
from os import path
from typing import TYPE_CHECKING, Any, ClassVar, cast
from docutils import nodes
from docutils.parsers.rst import directives
import sphinx
from sphinx import addnodes
from sphinx.ext.graphviz import figure_wrapper, graphviz, render_dot_html, render_dot_latex, render_dot_texinfo
from sphinx.util.docutils import SphinxDirective
if TYPE_CHECKING:
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
    from sphinx.writers.html5 import HTML5Translator
    from sphinx.writers.latex import LaTeXTranslator
    from sphinx.writers.texinfo import TexinfoTranslator
module_sig_re = re.compile('^(?:([\\w.]*)\\.)?  # module names\n                           (\\w+)  \\s* $          # class/final module name\n                           ', re.VERBOSE)
py_builtins = [obj for obj in vars(builtins).values() if inspect.isclass(obj)]

def try_import(objname: str) -> Any:
    """Import a object or module using *name* and *currentmodule*.
    *name* should be a relative name from *currentmodule* or
    a fully-qualified name.

    Returns imported object or module.  If failed, returns None value.
    """
    pass

def import_classes(name: str, currmodule: str) -> Any:
    """Import a class using its fully-qualified *name*."""
    pass

class InheritanceException(Exception):
    pass

class InheritanceGraph:
    """
    Given a list of classes, determines the set of classes that they inherit
    from all the way to the root "object", and then is able to generate a
    graphviz dot graph from them.
    """

    def __init__(self, class_names: list[str], currmodule: str, show_builtins: bool=False, private_bases: bool=False, parts: int=0, aliases: dict[str, str] | None=None, top_classes: Sequence[Any]=()) -> None:
        """*class_names* is a list of child classes to show bases from.

        If *show_builtins* is True, then Python builtins will be shown
        in the graph.
        """
        self.class_names = class_names
        classes = self._import_classes(class_names, currmodule)
        self.class_info = self._class_info(classes, show_builtins, private_bases, parts, aliases, top_classes)
        if not self.class_info:
            msg = 'No classes found for inheritance diagram'
            raise InheritanceException(msg)

    def _import_classes(self, class_names: list[str], currmodule: str) -> list[Any]:
        """Import a list of classes."""
        pass

    def _class_info(self, classes: list[Any], show_builtins: bool, private_bases: bool, parts: int, aliases: dict[str, str] | None, top_classes: Sequence[Any]) -> list[tuple[str, str, list[str], str]]:
        """Return name and bases for all classes that are ancestors of
        *classes*.

        *parts* gives the number of dotted name parts to include in the
        displayed node names, from right to left. If given as a negative, the
        number of parts to drop from the left. A value of 0 displays the full
        dotted name. E.g. ``sphinx.ext.inheritance_diagram.InheritanceGraph``
        with ``parts=2`` or ``parts=-2`` gets displayed as
        ``inheritance_diagram.InheritanceGraph``, and as
        ``ext.inheritance_diagram.InheritanceGraph`` with ``parts=3`` or
        ``parts=-1``.

        *top_classes* gives the name(s) of the top most ancestor class to
        traverse to. Multiple names can be specified separated by comma.
        """
        pass

    def class_name(self, cls: Any, parts: int=0, aliases: dict[str, str] | None=None) -> str:
        """Given a class object, return a fully-qualified name.

        This works for things I've tested in matplotlib so far, but may not be
        completely general.
        """
        pass

    def get_all_class_names(self) -> list[str]:
        """Get all of the class names involved in the graph."""
        pass
    default_graph_attrs = {'rankdir': 'LR', 'size': '"8.0, 12.0"', 'bgcolor': 'transparent'}
    default_node_attrs = {'shape': 'box', 'fontsize': 10, 'height': 0.25, 'fontname': '"Vera Sans, DejaVu Sans, Liberation Sans, Arial, Helvetica, sans"', 'style': '"setlinewidth(0.5),filled"', 'fillcolor': 'white'}
    default_edge_attrs = {'arrowsize': 0.5, 'style': '"setlinewidth(0.5)"'}

    def generate_dot(self, name: str, urls: dict[str, str] | None=None, env: BuildEnvironment | None=None, graph_attrs: dict | None=None, node_attrs: dict | None=None, edge_attrs: dict | None=None) -> str:
        """Generate a graphviz dot graph from the classes that were passed in
        to __init__.

        *name* is the name of the graph.

        *urls* is a dictionary mapping class names to HTTP URLs.

        *graph_attrs*, *node_attrs*, *edge_attrs* are dictionaries containing
        key/value pairs to pass on as graphviz properties.
        """
        pass

class inheritance_diagram(graphviz):
    """
    A docutils node to use as a placeholder for the inheritance diagram.
    """
    pass

class InheritanceDiagram(SphinxDirective):
    """
    Run when the inheritance_diagram directive is first encountered.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: ClassVar[OptionSpec] = {'parts': int, 'private-bases': directives.flag, 'caption': directives.unchanged, 'top-classes': directives.unchanged_required}

def html_visit_inheritance_diagram(self: HTML5Translator, node: inheritance_diagram) -> None:
    """
    Output the graph for HTML.  This will insert a PNG with clickable
    image map.
    """
    pass

def latex_visit_inheritance_diagram(self: LaTeXTranslator, node: inheritance_diagram) -> None:
    """
    Output the graph for LaTeX.  This will insert a PDF.
    """
    pass

def texinfo_visit_inheritance_diagram(self: TexinfoTranslator, node: inheritance_diagram) -> None:
    """
    Output the graph for Texinfo.  This will insert a PNG.
    """
    pass