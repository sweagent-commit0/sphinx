"""Sphinx test suite utilities"""
from __future__ import annotations
__all__ = ('SphinxTestApp', 'SphinxTestAppWrapperForSkipBuilding')
import contextlib
import os
import sys
from io import StringIO
from types import MappingProxyType
from typing import TYPE_CHECKING
from docutils import nodes
from docutils.parsers.rst import directives, roles
import sphinx.application
import sphinx.locale
import sphinx.pycode
from sphinx.util.console import strip_colors
from sphinx.util.docutils import additional_nodes
if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path
    from typing import Any
    from xml.etree.ElementTree import ElementTree
    from docutils.nodes import Node

def etree_parse(path: str | os.PathLike[str]) -> ElementTree:
    """Parse a file into a (safe) XML element tree."""
    pass

class SphinxTestApp(sphinx.application.Sphinx):
    """A subclass of :class:`~sphinx.application.Sphinx` for tests.

    The constructor uses some better default values for the initialization
    parameters and supports arbitrary keywords stored in the :attr:`extras`
    read-only mapping.

    It is recommended to use::

        @pytest.mark.sphinx('html', testroot='root')
        def test(app):
            app = ...

    instead of::

        def test():
            app = SphinxTestApp('html', srcdir=srcdir)

    In the former case, the 'app' fixture takes care of setting the source
    directory, whereas in the latter, the user must provide it themselves.
    """

    def __init__(self, /, buildername: str='html', srcdir: Path | None=None, builddir: Path | None=None, freshenv: bool=False, confoverrides: dict[str, Any] | None=None, status: StringIO | None=None, warning: StringIO | None=None, tags: Sequence[str]=(), docutils_conf: str | None=None, parallel: int=0, verbosity: int=0, warningiserror: bool=False, pdb: bool=False, exception_on_warning: bool=False, **extras: Any) -> None:
        assert srcdir is not None
        if verbosity == -1:
            quiet = True
            verbosity = 0
        else:
            quiet = False
        if status is None:
            status = None if quiet else StringIO()
        elif not isinstance(status, StringIO):
            err = '%r must be an io.StringIO object, got: %s' % ('status', type(status))
            raise TypeError(err)
        if warning is None:
            warning = None if quiet else StringIO()
        elif not isinstance(warning, StringIO):
            err = '%r must be an io.StringIO object, got: %s' % ('warning', type(warning))
            raise TypeError(err)
        self.docutils_conf_path = srcdir / 'docutils.conf'
        if docutils_conf is not None:
            self.docutils_conf_path.write_text(docutils_conf, encoding='utf8')
        if builddir is None:
            builddir = srcdir / '_build'
        confdir = srcdir
        outdir = builddir.joinpath(buildername)
        outdir.mkdir(parents=True, exist_ok=True)
        doctreedir = builddir.joinpath('doctrees')
        doctreedir.mkdir(parents=True, exist_ok=True)
        if confoverrides is None:
            confoverrides = {}
        self._saved_path = sys.path.copy()
        self.extras: Mapping[str, Any] = MappingProxyType(extras)
        'Extras keyword arguments.'
        try:
            super().__init__(srcdir, confdir, outdir, doctreedir, buildername, confoverrides=confoverrides, status=status, warning=warning, freshenv=freshenv, warningiserror=warningiserror, tags=tags, verbosity=verbosity, parallel=parallel, pdb=pdb, exception_on_warning=exception_on_warning)
        except Exception:
            self.cleanup()
            raise

    @property
    def status(self) -> StringIO:
        """The in-memory text I/O for the application status messages."""
        pass

    @property
    def warning(self) -> StringIO:
        """The in-memory text I/O for the application warning messages."""
        pass

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} buildername={self.builder.name!r}>'

class SphinxTestAppWrapperForSkipBuilding(SphinxTestApp):
    """A wrapper for SphinxTestApp.

    This class is used to speed up the test by skipping ``app.build()``
    if it has already been built and there are any output files.
    """
_DEPRECATED_OBJECTS: dict[str, tuple[Any, str, tuple[int, int]]] = {'strip_escseq': (strip_colors, 'sphinx.util.console.strip_colors', (9, 0))}

def __getattr__(name: str) -> Any:
    if name not in _DEPRECATED_OBJECTS:
        msg = f'module {__name__!r} has no attribute {name!r}'
        raise AttributeError(msg)
    from sphinx.deprecation import _deprecation_warning
    deprecated_object, canonical_name, remove = _DEPRECATED_OBJECTS[name]
    _deprecation_warning(__name__, name, canonical_name, remove=remove)
    return deprecated_object