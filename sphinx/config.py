"""Build configuration file handling."""
from __future__ import annotations
import sys
import time
import traceback
import types
import warnings
from os import getenv, path
from typing import TYPE_CHECKING, Any, Literal, NamedTuple
from sphinx.deprecation import RemovedInSphinx90Warning
from sphinx.errors import ConfigError, ExtensionError
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.osutil import fs_encoding
if sys.version_info >= (3, 11):
    from contextlib import chdir
else:
    from sphinx.util.osutil import _chdir as chdir
if TYPE_CHECKING:
    import os
    from collections.abc import Collection, Iterable, Iterator, Sequence, Set
    from typing import TypeAlias
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment
    from sphinx.util.tags import Tags
    from sphinx.util.typing import ExtensionMetadata, _ExtensionSetupFunc
logger = logging.getLogger(__name__)
_ConfigRebuild: TypeAlias = Literal['', 'env', 'epub', 'gettext', 'html', 'applehelp', 'devhelp']
CONFIG_FILENAME = 'conf.py'
UNSERIALIZABLE_TYPES = (type, types.ModuleType, types.FunctionType)

class ConfigValue(NamedTuple):
    name: str
    value: Any
    rebuild: _ConfigRebuild

def is_serializable(obj: object, *, _seen: frozenset[int]=frozenset()) -> bool:
    """Check if an object is serializable or not."""
    pass

class ENUM:
    """Represents the candidates which a config value should be one of.

    Example:
        app.add_config_value('latex_show_urls', 'no', None, ENUM('no', 'footnote', 'inline'))
    """

    def __init__(self, *candidates: str | bool | None) -> None:
        self.candidates = candidates
_OptValidTypes: TypeAlias = tuple[()] | tuple[type, ...] | frozenset[type] | ENUM

class _Opt:
    __slots__ = ('default', 'rebuild', 'valid_types', 'description')
    default: Any
    rebuild: _ConfigRebuild
    valid_types: _OptValidTypes
    description: str

    def __init__(self, default: Any, rebuild: _ConfigRebuild, valid_types: _OptValidTypes, description: str='') -> None:
        """Configuration option type for Sphinx.

        The type is intended to be immutable; changing the field values
        is an unsupported action.
        No validation is performed on the values, though consumers will
        likely expect them to be of the types advertised.
        The old tuple-based interface will be removed in Sphinx 9.
        """
        super().__setattr__('default', default)
        super().__setattr__('rebuild', rebuild)
        super().__setattr__('valid_types', valid_types)
        super().__setattr__('description', description)

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}(default={self.default!r}, rebuild={self.rebuild!r}, valid_types={self.rebuild!r}, description={self.description!r})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _Opt):
            self_tpl = (self.default, self.rebuild, self.valid_types, self.description)
            other_tpl = (other.default, other.rebuild, other.valid_types, self.description)
            return self_tpl == other_tpl
        return NotImplemented

    def __lt__(self, other: _Opt) -> bool:
        if self.__class__ is other.__class__:
            self_tpl = (self.default, self.rebuild, self.valid_types, self.description)
            other_tpl = (other.default, other.rebuild, other.valid_types, self.description)
            return self_tpl > other_tpl
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.default, self.rebuild, self.valid_types, self.description))

    def __setattr__(self, key: str, value: Any) -> None:
        if key in {'default', 'rebuild', 'valid_types', 'description'}:
            msg = f'{self.__class__.__name__!r} object does not support assignment to {key!r}'
            raise TypeError(msg)
        super().__setattr__(key, value)

    def __delattr__(self, key: str) -> None:
        if key in {'default', 'rebuild', 'valid_types', 'description'}:
            msg = f'{self.__class__.__name__!r} object does not support deletion of {key!r}'
            raise TypeError(msg)
        super().__delattr__(key)

    def __getstate__(self) -> tuple[Any, _ConfigRebuild, _OptValidTypes, str]:
        return (self.default, self.rebuild, self.valid_types, self.description)

    def __setstate__(self, state: tuple[Any, _ConfigRebuild, _OptValidTypes, str]) -> None:
        default, rebuild, valid_types, description = state
        super().__setattr__('default', default)
        super().__setattr__('rebuild', rebuild)
        super().__setattr__('valid_types', valid_types)
        super().__setattr__('description', description)

    def __getitem__(self, item: int | slice) -> Any:
        warnings.warn(f"The {self.__class__.__name__!r} object tuple interface is deprecated, use attribute access instead for 'default', 'rebuild', and 'valid_types'.", RemovedInSphinx90Warning, stacklevel=2)
        return (self.default, self.rebuild, self.valid_types)[item]

class Config:
    """Configuration file abstraction.

    The Config object makes the values of all config options available as
    attributes.

    It is exposed via the :py:class:`~sphinx.application.Sphinx`\\ ``.config``
    and :py:class:`sphinx.environment.BuildEnvironment`\\ ``.config`` attributes.
    For example, to get the value of :confval:`language`, use either
    ``app.config.language`` or ``env.config.language``.
    """
    config_values: dict[str, _Opt] = {'project': _Opt('Project name not set', 'env', ()), 'author': _Opt('Author name not set', 'env', ()), 'project_copyright': _Opt('', 'html', frozenset((str, tuple, list))), 'copyright': _Opt(lambda config: config.project_copyright, 'html', frozenset((str, tuple, list))), 'version': _Opt('', 'env', ()), 'release': _Opt('', 'env', ()), 'today': _Opt('', 'env', ()), 'today_fmt': _Opt(None, 'env', frozenset((str,))), 'language': _Opt('en', 'env', frozenset((str,))), 'locale_dirs': _Opt(['locales'], 'env', ()), 'figure_language_filename': _Opt('{root}.{language}{ext}', 'env', frozenset((str,))), 'gettext_allow_fuzzy_translations': _Opt(False, 'gettext', ()), 'translation_progress_classes': _Opt(False, 'env', ENUM(True, False, 'translated', 'untranslated')), 'master_doc': _Opt('index', 'env', ()), 'root_doc': _Opt(lambda config: config.master_doc, 'env', ()), 'source_suffix': _Opt({'.rst': 'restructuredtext'}, 'env', Any), 'source_encoding': _Opt('utf-8-sig', 'env', ()), 'exclude_patterns': _Opt([], 'env', frozenset((str,))), 'include_patterns': _Opt(['**'], 'env', frozenset((str,))), 'default_role': _Opt(None, 'env', frozenset((str,))), 'add_function_parentheses': _Opt(True, 'env', ()), 'add_module_names': _Opt(True, 'env', ()), 'toc_object_entries': _Opt(True, 'env', frozenset((bool,))), 'toc_object_entries_show_parents': _Opt('domain', 'env', ENUM('domain', 'all', 'hide')), 'trim_footnote_reference_space': _Opt(False, 'env', ()), 'show_authors': _Opt(False, 'env', ()), 'pygments_style': _Opt(None, 'html', frozenset((str,))), 'highlight_language': _Opt('default', 'env', ()), 'highlight_options': _Opt({}, 'env', ()), 'templates_path': _Opt([], 'html', ()), 'template_bridge': _Opt(None, 'html', frozenset((str,))), 'keep_warnings': _Opt(False, 'env', ()), 'suppress_warnings': _Opt([], 'env', ()), 'show_warning_types': _Opt(True, 'env', frozenset((bool,))), 'modindex_common_prefix': _Opt([], 'html', ()), 'rst_epilog': _Opt(None, 'env', frozenset((str,))), 'rst_prolog': _Opt(None, 'env', frozenset((str,))), 'trim_doctest_flags': _Opt(True, 'env', ()), 'primary_domain': _Opt('py', 'env', frozenset((types.NoneType,))), 'needs_sphinx': _Opt(None, '', frozenset((str,))), 'needs_extensions': _Opt({}, '', ()), 'manpages_url': _Opt(None, 'env', ()), 'nitpicky': _Opt(False, '', ()), 'nitpick_ignore': _Opt([], '', frozenset((set, list, tuple))), 'nitpick_ignore_regex': _Opt([], '', frozenset((set, list, tuple))), 'numfig': _Opt(False, 'env', ()), 'numfig_secnum_depth': _Opt(1, 'env', ()), 'numfig_format': _Opt({}, 'env', ()), 'maximum_signature_line_length': _Opt(None, 'env', frozenset((int, types.NoneType))), 'math_number_all': _Opt(False, 'env', ()), 'math_eqref_format': _Opt(None, 'env', frozenset((str,))), 'math_numfig': _Opt(True, 'env', ()), 'math_numsep': _Opt('.', 'env', frozenset((str,))), 'tls_verify': _Opt(True, 'env', ()), 'tls_cacerts': _Opt(None, 'env', ()), 'user_agent': _Opt(None, 'env', frozenset((str,))), 'smartquotes': _Opt(True, 'env', ()), 'smartquotes_action': _Opt('qDe', 'env', ()), 'smartquotes_excludes': _Opt({'languages': ['ja'], 'builders': ['man', 'text']}, 'env', ()), 'option_emphasise_placeholders': _Opt(False, 'env', ())}

    def __init__(self, config: dict[str, Any] | None=None, overrides: dict[str, Any] | None=None) -> None:
        raw_config: dict[str, Any] = config or {}
        self._overrides = dict(overrides) if overrides is not None else {}
        self._options = Config.config_values.copy()
        self._raw_config = raw_config
        for name in list(self._overrides.keys()):
            if '.' in name:
                real_name, key = name.split('.', 1)
                raw_config.setdefault(real_name, {})[key] = self._overrides.pop(name)
        self.setup: _ExtensionSetupFunc | None = raw_config.get('setup')
        if 'extensions' in self._overrides:
            extensions = self._overrides.pop('extensions')
            if isinstance(extensions, str):
                raw_config['extensions'] = extensions.split(',')
            else:
                raw_config['extensions'] = extensions
        self.extensions: list[str] = raw_config.get('extensions', [])

    @classmethod
    def read(cls: type[Config], confdir: str | os.PathLike[str], overrides: dict | None=None, tags: Tags | None=None) -> Config:
        """Create a Config object from configuration file."""
        pass

    def __repr__(self) -> str:
        values = []
        for opt_name in self._options:
            try:
                opt_value = getattr(self, opt_name)
            except Exception:
                opt_value = '<error!>'
            values.append(f'{opt_name}={opt_value!r}')
        return self.__class__.__qualname__ + '(' + ', '.join(values) + ')'

    def __setattr__(self, key: str, value: object) -> None:
        if key == 'master_doc':
            super().__setattr__('root_doc', value)
        elif key == 'root_doc':
            super().__setattr__('master_doc', value)
        elif key == 'copyright':
            super().__setattr__('project_copyright', value)
        elif key == 'project_copyright':
            super().__setattr__('copyright', value)
        super().__setattr__(key, value)

    def __getattr__(self, name: str) -> Any:
        if name in self._options:
            if name in self._overrides:
                value = self._overrides[name]
                if not isinstance(value, str):
                    self.__dict__[name] = value
                    return value
                try:
                    value = self.convert_overrides(name, value)
                except ValueError as exc:
                    logger.warning('%s', exc)
                else:
                    self.__setattr__(name, value)
                    return value
            if name in self._raw_config:
                value = self._raw_config[name]
                self.__setattr__(name, value)
                return value
            default = self._options[name].default
            if callable(default):
                return default(self)
            self.__dict__[name] = default
            return default
        if name.startswith('_'):
            msg = f'{self.__class__.__name__!r} object has no attribute {name!r}'
            raise AttributeError(msg)
        msg = __('No such config value: %r') % name
        raise AttributeError(msg)

    def __getitem__(self, name: str) -> Any:
        return getattr(self, name)

    def __setitem__(self, name: str, value: Any) -> None:
        setattr(self, name, value)

    def __delitem__(self, name: str) -> None:
        delattr(self, name)

    def __contains__(self, name: str) -> bool:
        return name in self._options

    def __iter__(self) -> Iterator[ConfigValue]:
        for name, opt in self._options.items():
            yield ConfigValue(name, getattr(self, name), opt.rebuild)

    def __getstate__(self) -> dict:
        """Obtains serializable data for pickling."""
        __dict__ = {key: value for key, value in self.__dict__.items() if not key.startswith('_') and is_serializable(value)}
        __dict__['_options'] = _options = {}
        for name, opt in self._options.items():
            if not isinstance(opt, _Opt) and isinstance(opt, tuple) and (len(opt) <= 3):
                self._options[name] = opt = _Opt(*opt)
            real_value = getattr(self, name)
            if not is_serializable(real_value):
                if opt.rebuild:
                    logger.warning(__('cannot cache unpickable configuration value: %r (because it contains a function, class, or module object)'), name, type='config', subtype='cache', once=True)
                real_value = None
            _options[name] = (real_value, opt.rebuild)
        return __dict__

    def __setstate__(self, state: dict) -> None:
        self._overrides = {}
        self._options = {name: _Opt(real_value, rebuild, ()) for name, (real_value, rebuild) in state.pop('_options').items()}
        self._raw_config = {}
        self.__dict__.update(state)

def eval_config_file(filename: str, tags: Tags | None) -> dict[str, Any]:
    """Evaluate a config file."""
    pass

def convert_source_suffix(app: Sphinx, config: Config) -> None:
    """Convert old styled source_suffix to new styled one.

    * old style: str or list
    * new style: a dict which maps from fileext to filetype
    """
    pass

def convert_highlight_options(app: Sphinx, config: Config) -> None:
    """Convert old styled highlight_options to new styled one.

    * old style: options
    * new style: a dict which maps from language name to options
    """
    pass

def init_numfig_format(app: Sphinx, config: Config) -> None:
    """Initialize :confval:`numfig_format`."""
    pass

def correct_copyright_year(_app: Sphinx, config: Config) -> None:
    """Correct values of copyright year that are not coherent with
    the SOURCE_DATE_EPOCH environment variable (if set)

    See https://reproducible-builds.org/specs/source-date-epoch/
    """
    pass

def _substitute_copyright_year(copyright_line: str, replace_year: str) -> str:
    """Replace the year in a single copyright line.

    Legal formats are:

    * ``YYYY``
    * ``YYYY,``
    * ``YYYY ``
    * ``YYYY-YYYY,``
    * ``YYYY-YYYY ``

    The final year in the string is replaced with ``replace_year``.
    """
    pass

def check_confval_types(app: Sphinx | None, config: Config) -> None:
    """Check all values for deviation from the default value's type, since
    that can result in TypeErrors all over the place NB.
    """
    pass

def check_root_doc(app: Sphinx, env: BuildEnvironment, added: Set[str], changed: Set[str], removed: Set[str]) -> Iterable[str]:
    """Adjust root_doc to 'contents' to support an old project which does not have
    any root_doc setting.
    """
    pass