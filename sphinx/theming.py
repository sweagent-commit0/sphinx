"""Theming support for HTML builders."""
from __future__ import annotations
__all__ = ('Theme', 'HTMLThemeFactory')
import configparser
import contextlib
import os
import shutil
import sys
import tempfile
from importlib.metadata import entry_points
from os import path
from typing import TYPE_CHECKING, Any
from zipfile import ZipFile
from sphinx import package_dir
from sphinx.config import check_confval_types as _config_post_init
from sphinx.errors import ThemeError
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.osutil import ensuredir
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib
if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import TypedDict
    from typing_extensions import Required
    from sphinx.application import Sphinx

    class _ThemeToml(TypedDict, total=False):
        theme: Required[_ThemeTomlTheme]
        options: dict[str, str]

    class _ThemeTomlTheme(TypedDict, total=False):
        inherit: Required[str]
        stylesheets: list[str]
        sidebars: list[str]
        pygments_style: _ThemeTomlThemePygments

    class _ThemeTomlThemePygments(TypedDict, total=False):
        default: str
        dark: str
logger = logging.getLogger(__name__)
_NO_DEFAULT = object()
_THEME_TOML = 'theme.toml'
_THEME_CONF = 'theme.conf'

class Theme:
    """A Theme is a set of HTML templates and configurations.

    This class supports both theme directory and theme archive (zipped theme).
    """

    def __init__(self, name: str, *, configs: dict[str, _ConfigFile], paths: list[str], tmp_dirs: list[str]) -> None:
        self.name = name
        self._dirs = tuple(paths)
        self._tmp_dirs = tmp_dirs
        options: dict[str, Any] = {}
        self.stylesheets: tuple[str, ...] = ()
        self.sidebar_templates: tuple[str, ...] = ()
        self.pygments_style_default: str | None = None
        self.pygments_style_dark: str | None = None
        for config in reversed(configs.values()):
            options |= config.options
            if config.stylesheets is not None:
                self.stylesheets = config.stylesheets
            if config.sidebar_templates is not None:
                self.sidebar_templates = config.sidebar_templates
            if config.pygments_style_default is not None:
                self.pygments_style_default = config.pygments_style_default
            if config.pygments_style_dark is not None:
                self.pygments_style_dark = config.pygments_style_dark
        self._options = options

    def get_theme_dirs(self) -> list[str]:
        """Return a list of theme directories, beginning with this theme's,
        then the base theme's, then that one's base theme's, etc.
        """
        pass

    def get_config(self, section: str, name: str, default: Any=_NO_DEFAULT) -> Any:
        """Return the value for a theme configuration setting, searching the
        base theme chain.
        """
        pass

    def get_options(self, overrides: dict[str, Any] | None=None) -> dict[str, Any]:
        """Return a dictionary of theme options and their values."""
        pass

    def _cleanup(self) -> None:
        """Remove temporary directories."""
        pass

class HTMLThemeFactory:
    """A factory class for HTML Themes."""

    def __init__(self, app: Sphinx) -> None:
        self._app = app
        self._themes = app.registry.html_themes
        self._entry_point_themes: dict[str, Callable[[], None]] = {}
        self._load_builtin_themes()
        if getattr(app.config, 'html_theme_path', None):
            self._load_additional_themes(app.config.html_theme_path)
        self._load_entry_point_themes()

    def _load_builtin_themes(self) -> None:
        """Load built-in themes."""
        pass

    def _load_additional_themes(self, theme_paths: list[str]) -> None:
        """Load additional themes placed at specified directories."""
        pass

    def _load_entry_point_themes(self) -> None:
        """Try to load a theme with the specified name.

        This uses the ``sphinx.html_themes`` entry point from package metadata.
        """
        pass

    @staticmethod
    def _find_themes(theme_path: str) -> dict[str, str]:
        """Search themes from specified directory."""
        pass

    def create(self, name: str) -> Theme:
        """Create an instance of theme."""
        pass

def _is_archived_theme(filename: str, /) -> bool:
    """Check whether the specified file is an archived theme file or not."""
    pass

def _extract_zip(filename: str, target_dir: str, /) -> None:
    """Extract zip file to target directory."""
    pass

class _ConfigFile:
    __slots__ = ('stylesheets', 'sidebar_templates', 'pygments_style_default', 'pygments_style_dark', 'options')

    def __init__(self, stylesheets: tuple[str, ...] | None, sidebar_templates: tuple[str, ...] | None, pygments_style_default: str | None, pygments_style_dark: str | None, options: dict[str, str]) -> None:
        self.stylesheets: tuple[str, ...] | None = stylesheets
        self.sidebar_templates: tuple[str, ...] | None = sidebar_templates
        self.pygments_style_default: str | None = pygments_style_default
        self.pygments_style_dark: str | None = pygments_style_dark
        self.options: dict[str, str] = options.copy()

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}(stylesheets={self.stylesheets!r}, sidebar_templates={self.sidebar_templates!r}, pygments_style_default={self.pygments_style_default!r}, pygments_style_dark={self.pygments_style_dark!r}, options={self.options!r})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _ConfigFile):
            return self.stylesheets == other.stylesheets and self.sidebar_templates == other.sidebar_templates and (self.pygments_style_default == other.pygments_style_default) and (self.pygments_style_dark == other.pygments_style_dark) and (self.options == other.options)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.__class__.__qualname__, self.stylesheets, self.sidebar_templates, self.pygments_style_default, self.pygments_style_dark, self.options))
if __name__ == '__main__':
    raise SystemExit(_migrate_conf_to_toml(sys.argv[1:]))