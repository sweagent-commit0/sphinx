"""Transforms for LaTeX builder."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, cast
from docutils import nodes
from docutils.transforms.references import Substitutions
from sphinx import addnodes
from sphinx.builders.latex.nodes import captioned_literal_block, footnotemark, footnotetext, math_reference, thebibliography
from sphinx.domains.citation import CitationDomain
from sphinx.locale import __
from sphinx.transforms import SphinxTransform
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.nodes import NodeMatcher
if TYPE_CHECKING:
    from docutils.nodes import Element, Node
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
URI_SCHEMES = ('mailto:', 'http:', 'https:', 'ftp:')

class FootnoteDocnameUpdater(SphinxTransform):
    """Add docname to footnote and footnote_reference nodes."""
    default_priority = 700
    TARGET_NODES = (nodes.footnote, nodes.footnote_reference)

class SubstitutionDefinitionsRemover(SphinxPostTransform):
    """Remove ``substitution_definition`` nodes from doctrees."""
    default_priority = Substitutions.default_priority + 1
    formats = ('latex',)

class ShowUrlsTransform(SphinxPostTransform):
    """Expand references to inline text or footnotes.

    For more information, see :confval:`latex_show_urls`.

    .. note:: This transform is used for integrated doctree
    """
    default_priority = 400
    formats = ('latex',)
    expanded = False

class FootnoteCollector(nodes.NodeVisitor):
    """Collect footnotes and footnote references on the document"""

    def __init__(self, document: nodes.document) -> None:
        self.auto_footnotes: list[nodes.footnote] = []
        self.used_footnote_numbers: set[str] = set()
        self.footnote_refs: list[nodes.footnote_reference] = []
        super().__init__(document)

class LaTeXFootnoteTransform(SphinxPostTransform):
    """Convert footnote definitions and references to appropriate form to LaTeX.

    * Replace footnotes on restricted zone (e.g. headings) by footnotemark node.
      In addition, append a footnotetext node after the zone.

      Before::

          <section>
              <title>
                  headings having footnotes
                  <footnote_reference>
                      1
              <footnote ids="id1">
                  <label>
                      1
                  <paragraph>
                      footnote body

      After::

          <section>
              <title>
                  headings having footnotes
                  <footnotemark refid="id1">
                      1
              <footnotetext ids="id1">
                  <label>
                      1
                  <paragraph>
                      footnote body

    * Integrate footnote definitions and footnote references to single footnote node

      Before::

          blah blah blah
          <footnote_reference refid="id1">
              1
          blah blah blah ...

          <footnote ids="id1">
              <label>
                  1
              <paragraph>
                  footnote body

      After::

          blah blah blah
          <footnote ids="id1">
              <label>
                  1
              <paragraph>
                  footnote body
          blah blah blah ...

    * Replace second and subsequent footnote references which refers same footnote definition
      by footnotemark node.  Additionally, the footnote definition node is marked as
      "referred".

      Before::

          blah blah blah
          <footnote_reference refid="id1">
              1
          blah blah blah
          <footnote_reference refid="id1">
              1
          blah blah blah ...

          <footnote ids="id1">
              <label>
                  1
              <paragraph>
                  footnote body

      After::

          blah blah blah
          <footnote ids="id1" referred=True>
              <label>
                  1
              <paragraph>
                  footnote body
          blah blah blah
          <footnotemark refid="id1">
              1
          blah blah blah ...

    * Remove unreferenced footnotes

      Before::

          <footnote ids="id1">
              <label>
                  1
              <paragraph>
                  Unreferenced footnote!

      After::

          <!-- nothing! -->

    * Move footnotes in a title of table or thead to head of tbody

      Before::

          <table>
              <title>
                  title having footnote_reference
                  <footnote_reference refid="id1">
                      1
              <tgroup>
                  <thead>
                      <row>
                          <entry>
                              header having footnote_reference
                              <footnote_reference refid="id2">
                                  2
                  <tbody>
                      <row>
                      ...

          <footnote ids="id1">
              <label>
                  1
              <paragraph>
                  footnote body

          <footnote ids="id2">
              <label>
                  2
              <paragraph>
                  footnote body

      After::

          <table>
              <title>
                  title having footnote_reference
                  <footnotemark refid="id1">
                      1
              <tgroup>
                  <thead>
                      <row>
                          <entry>
                              header having footnote_reference
                              <footnotemark refid="id2">
                                  2
                  <tbody>
                      <footnotetext ids="id1">
                          <label>
                              1
                          <paragraph>
                              footnote body

                      <footnotetext ids="id2">
                          <label>
                              2
                          <paragraph>
                              footnote body
                      <row>
                      ...
    """
    default_priority = 600
    formats = ('latex',)

class LaTeXFootnoteVisitor(nodes.NodeVisitor):

    def __init__(self, document: nodes.document, footnotes: list[nodes.footnote]) -> None:
        self.appeared: dict[tuple[str, str], nodes.footnote] = {}
        self.footnotes: list[nodes.footnote] = footnotes
        self.pendings: list[nodes.footnote] = []
        self.table_footnotes: list[nodes.footnote] = []
        self.restricted: Element | None = None
        super().__init__(document)

class BibliographyTransform(SphinxPostTransform):
    """Gather bibliography entries to tail of document.

    Before::

        <document>
            <paragraph>
                blah blah blah
            <citation>
                ...
            <paragraph>
                blah blah blah
            <citation>
                ...
            ...

    After::

        <document>
            <paragraph>
                blah blah blah
            <paragraph>
                blah blah blah
            ...
            <thebibliography>
                <citation>
                    ...
                <citation>
                    ...
    """
    default_priority = 750
    formats = ('latex',)

class CitationReferenceTransform(SphinxPostTransform):
    """Replace pending_xref nodes for citation by citation_reference.

    To handle citation reference easily on LaTeX writer, this converts
    pending_xref nodes to citation_reference.
    """
    default_priority = 5
    formats = ('latex',)

class MathReferenceTransform(SphinxPostTransform):
    """Replace pending_xref nodes for math by math_reference.

    To handle math reference easily on LaTeX writer, this converts pending_xref
    nodes to math_reference.
    """
    default_priority = 5
    formats = ('latex',)

class LiteralBlockTransform(SphinxPostTransform):
    """Replace container nodes for literal_block by captioned_literal_block."""
    default_priority = 400
    formats = ('latex',)

class DocumentTargetTransform(SphinxPostTransform):
    """Add :doc label to the first section of each document."""
    default_priority = 400
    formats = ('latex',)

class IndexInSectionTitleTransform(SphinxPostTransform):
    """Move index nodes in section title to outside of the title.

    LaTeX index macro is not compatible with some handling of section titles
    such as uppercasing done on LaTeX side (cf. fncychap handling of ``\\chapter``).
    Moving the index node to after the title node fixes that.

    Before::

        <section>
            <title>
                blah blah <index entries=[...]/>blah
            <paragraph>
                blah blah blah
            ...

    After::

        <section>
            <title>
                blah blah blah
            <index entries=[...]/>
            <paragraph>
                blah blah blah
            ...
    """
    default_priority = 400
    formats = ('latex',)