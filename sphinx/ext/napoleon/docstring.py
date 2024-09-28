"""Classes for docstring parsing and formatting."""
from __future__ import annotations
import collections
import contextlib
import inspect
import re
from functools import partial
from itertools import starmap
from typing import TYPE_CHECKING, Any
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.typing import get_type_hints, stringify_annotation
if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from sphinx.application import Sphinx
    from sphinx.config import Config as SphinxConfig
logger = logging.getLogger(__name__)
_directive_regex = re.compile('\\.\\. \\S+::')
_google_section_regex = re.compile('^(\\s|\\w)+:\\s*$')
_google_typed_arg_regex = re.compile('(.+?)\\(\\s*(.*[^\\s]+)\\s*\\)')
_numpy_section_regex = re.compile('^[=\\-`:\\\'"~^_*+#<>]{2,}\\s*$')
_single_colon_regex = re.compile('(?<!:):(?!:)')
_xref_or_code_regex = re.compile('((?::(?:[a-zA-Z0-9]+[\\-_+:.])*[a-zA-Z0-9]+:`.+?`)|(?:``.+?``)|(?::meta .+:.*)|(?:`.+?\\s*(?<!\\x00)<.*?>`))')
_xref_regex = re.compile('(?:(?::(?:[a-zA-Z0-9]+[\\-_+:.])*[a-zA-Z0-9]+:)?`.+?`)')
_bullet_list_regex = re.compile('^(\\*|\\+|\\-)(\\s+\\S|\\s*$)')
_enumerated_list_regex = re.compile('^(?P<paren>\\()?(\\d+|#|[ivxlcdm]+|[IVXLCDM]+|[a-zA-Z])(?(paren)\\)|\\.)(\\s+\\S|\\s*$)')
_token_regex = re.compile('(,\\sor\\s|\\sor\\s|\\sof\\s|:\\s|\\sto\\s|,\\sand\\s|\\sand\\s|,\\s|[{]|[}]|"(?:\\\\"|[^"])*"|\'(?:\\\\\'|[^\'])*\')')
_default_regex = re.compile('^default[^_0-9A-Za-z].*$')
_SINGLETONS = ('None', 'True', 'False', 'Ellipsis')

class Deque(collections.deque):
    """
    A subclass of deque that mimics ``pockets.iterators.modify_iter``.

    The `.Deque.get` and `.Deque.next` methods are added.
    """
    sentinel = object()

    def get(self, n: int) -> Any:
        """
        Return the nth element of the stack, or ``self.sentinel`` if n is
        greater than the stack size.
        """
        pass

def _convert_type_spec(_type: str, translations: dict[str, str] | None=None) -> str:
    """Convert type specification to reference in reST."""
    pass

class GoogleDocstring:
    """Convert Google style docstrings to reStructuredText.

    Parameters
    ----------
    docstring : :obj:`str` or :obj:`list` of :obj:`str`
        The docstring to parse, given either as a string or split into
        individual lines.
    config: :obj:`sphinx.ext.napoleon.Config` or :obj:`sphinx.config.Config`
        The configuration settings to use. If not given, defaults to the
        config object on `app`; or if `app` is not given defaults to the
        a new :class:`sphinx.ext.napoleon.Config` object.


    Other Parameters
    ----------------
    app : :class:`sphinx.application.Sphinx`, optional
        Application object representing the Sphinx process.
    what : :obj:`str`, optional
        A string specifying the type of the object to which the docstring
        belongs. Valid values: "module", "class", "exception", "function",
        "method", "attribute".
    name : :obj:`str`, optional
        The fully qualified name of the object.
    obj : module, class, exception, function, method, or attribute
        The object to which the docstring belongs.
    options : :class:`sphinx.ext.autodoc.Options`, optional
        The options given to the directive: an object with attributes
        inherited_members, undoc_members, show_inheritance and no_index that
        are True if the flag option of same name was given to the auto
        directive.


    Example
    -------
    >>> from sphinx.ext.napoleon import Config
    >>> config = Config(napoleon_use_param=True, napoleon_use_rtype=True)
    >>> docstring = '''One line summary.
    ...
    ... Extended description.
    ...
    ... Args:
    ...   arg1(int): Description of `arg1`
    ...   arg2(str): Description of `arg2`
    ... Returns:
    ...   str: Description of return value.
    ... '''
    >>> print(GoogleDocstring(docstring, config))
    One line summary.
    <BLANKLINE>
    Extended description.
    <BLANKLINE>
    :param arg1: Description of `arg1`
    :type arg1: int
    :param arg2: Description of `arg2`
    :type arg2: str
    <BLANKLINE>
    :returns: Description of return value.
    :rtype: str
    <BLANKLINE>

    """
    _name_rgx = re.compile('^\\s*((?::(?P<role>\\S+):)?`(?P<name>~?[a-zA-Z0-9_.-]+)`| (?P<name2>~?[a-zA-Z0-9_.-]+))\\s*', re.VERBOSE)

    def __init__(self, docstring: str | list[str], config: SphinxConfig | None=None, app: Sphinx | None=None, what: str='', name: str='', obj: Any=None, options: Any=None) -> None:
        self._app = app
        if config:
            self._config = config
        elif app:
            self._config = app.config
        else:
            from sphinx.ext.napoleon import Config
            self._config = Config()
        if not what:
            if inspect.isclass(obj):
                what = 'class'
            elif inspect.ismodule(obj):
                what = 'module'
            elif callable(obj):
                what = 'function'
            else:
                what = 'object'
        self._what = what
        self._name = name
        self._obj = obj
        self._opt = options
        if isinstance(docstring, str):
            lines = docstring.splitlines()
        else:
            lines = docstring
        self._lines = Deque(map(str.rstrip, lines))
        self._parsed_lines: list[str] = []
        self._is_in_section = False
        self._section_indent = 0
        if not hasattr(self, '_directive_sections'):
            self._directive_sections: list[str] = []
        if not hasattr(self, '_sections'):
            self._sections: dict[str, Callable] = {'args': self._parse_parameters_section, 'arguments': self._parse_parameters_section, 'attention': partial(self._parse_admonition, 'attention'), 'attributes': self._parse_attributes_section, 'caution': partial(self._parse_admonition, 'caution'), 'danger': partial(self._parse_admonition, 'danger'), 'error': partial(self._parse_admonition, 'error'), 'example': self._parse_examples_section, 'examples': self._parse_examples_section, 'hint': partial(self._parse_admonition, 'hint'), 'important': partial(self._parse_admonition, 'important'), 'keyword args': self._parse_keyword_arguments_section, 'keyword arguments': self._parse_keyword_arguments_section, 'methods': self._parse_methods_section, 'note': partial(self._parse_admonition, 'note'), 'notes': self._parse_notes_section, 'other parameters': self._parse_other_parameters_section, 'parameters': self._parse_parameters_section, 'receive': self._parse_receives_section, 'receives': self._parse_receives_section, 'return': self._parse_returns_section, 'returns': self._parse_returns_section, 'raise': self._parse_raises_section, 'raises': self._parse_raises_section, 'references': self._parse_references_section, 'see also': self._parse_see_also_section, 'tip': partial(self._parse_admonition, 'tip'), 'todo': partial(self._parse_admonition, 'todo'), 'warning': partial(self._parse_admonition, 'warning'), 'warnings': partial(self._parse_admonition, 'warning'), 'warn': self._parse_warns_section, 'warns': self._parse_warns_section, 'yield': self._parse_yields_section, 'yields': self._parse_yields_section}
        self._load_custom_sections()
        self._parse()

    def __str__(self) -> str:
        """Return the parsed docstring in reStructuredText format.

        Returns
        -------
        unicode
            Unicode version of the docstring.

        """
        return '\n'.join(self.lines())

    def lines(self) -> list[str]:
        """Return the parsed lines of the docstring in reStructuredText format.

        Returns
        -------
        list(str)
            The lines of the docstring in a list.

        """
        pass

class NumpyDocstring(GoogleDocstring):
    """Convert NumPy style docstrings to reStructuredText.

    Parameters
    ----------
    docstring : :obj:`str` or :obj:`list` of :obj:`str`
        The docstring to parse, given either as a string or split into
        individual lines.
    config: :obj:`sphinx.ext.napoleon.Config` or :obj:`sphinx.config.Config`
        The configuration settings to use. If not given, defaults to the
        config object on `app`; or if `app` is not given defaults to the
        a new :class:`sphinx.ext.napoleon.Config` object.


    Other Parameters
    ----------------
    app : :class:`sphinx.application.Sphinx`, optional
        Application object representing the Sphinx process.
    what : :obj:`str`, optional
        A string specifying the type of the object to which the docstring
        belongs. Valid values: "module", "class", "exception", "function",
        "method", "attribute".
    name : :obj:`str`, optional
        The fully qualified name of the object.
    obj : module, class, exception, function, method, or attribute
        The object to which the docstring belongs.
    options : :class:`sphinx.ext.autodoc.Options`, optional
        The options given to the directive: an object with attributes
        inherited_members, undoc_members, show_inheritance and no_index that
        are True if the flag option of same name was given to the auto
        directive.


    Example
    -------
    >>> from sphinx.ext.napoleon import Config
    >>> config = Config(napoleon_use_param=True, napoleon_use_rtype=True)
    >>> docstring = '''One line summary.
    ...
    ... Extended description.
    ...
    ... Parameters
    ... ----------
    ... arg1 : int
    ...     Description of `arg1`
    ... arg2 : str
    ...     Description of `arg2`
    ... Returns
    ... -------
    ... str
    ...     Description of return value.
    ... '''
    >>> print(NumpyDocstring(docstring, config))
    One line summary.
    <BLANKLINE>
    Extended description.
    <BLANKLINE>
    :param arg1: Description of `arg1`
    :type arg1: int
    :param arg2: Description of `arg2`
    :type arg2: str
    <BLANKLINE>
    :returns: Description of return value.
    :rtype: str
    <BLANKLINE>

    Methods
    -------
    __str__()
        Return the parsed docstring in reStructuredText format.

        Returns
        -------
        str
            UTF-8 encoded version of the docstring.

    __unicode__()
        Return the parsed docstring in reStructuredText format.

        Returns
        -------
        unicode
            Unicode version of the docstring.

    lines()
        Return the parsed lines of the docstring in reStructuredText format.

        Returns
        -------
        list(str)
            The lines of the docstring in a list.

    """

    def __init__(self, docstring: str | list[str], config: SphinxConfig | None=None, app: Sphinx | None=None, what: str='', name: str='', obj: Any=None, options: Any=None) -> None:
        self._directive_sections = ['.. index::']
        super().__init__(docstring, config, app, what, name, obj, options)

    def _parse_numpydoc_see_also_section(self, content: list[str]) -> list[str]:
        """
        Derived from the NumpyDoc implementation of _parse_see_also.

        See Also
        --------
        func_name : Descriptive text
            continued text
        another_func_name : Descriptive text
        func_name1, func_name2, :meth:`func_name`, func_name3

        """
        pass