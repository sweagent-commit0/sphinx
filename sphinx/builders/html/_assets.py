from __future__ import annotations
import os
import warnings
import zlib
from typing import TYPE_CHECKING, Any, NoReturn
from sphinx.deprecation import RemovedInSphinx90Warning
from sphinx.errors import ThemeError
if TYPE_CHECKING:
    from pathlib import Path

class _CascadingStyleSheet:
    filename: str | os.PathLike[str]
    priority: int
    attributes: dict[str, str]

    def __init__(self, filename: str | os.PathLike[str], /, *, priority: int=500, rel: str='stylesheet', type: str='text/css', **attributes: str) -> None:
        object.__setattr__(self, 'filename', filename)
        object.__setattr__(self, 'priority', priority)
        object.__setattr__(self, 'attributes', {'rel': rel, 'type': type} | attributes)

    def __str__(self) -> str:
        attr = ', '.join((f'{k}={v!r}' for k, v in self.attributes.items()))
        return f'{self.__class__.__name__}({self.filename!r}, priority={self.priority}, {attr})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            warnings.warn('The str interface for _CascadingStyleSheet objects is deprecated. Use css.filename instead.', RemovedInSphinx90Warning, stacklevel=2)
            return self.filename == other
        if not isinstance(other, _CascadingStyleSheet):
            return NotImplemented
        return self.filename == other.filename and self.priority == other.priority and (self.attributes == other.attributes)

    def __hash__(self) -> int:
        return hash((self.filename, self.priority, *sorted(self.attributes.items())))

    def __setattr__(self, key: str, value: Any) -> NoReturn:
        msg = f'{self.__class__.__name__} is immutable'
        raise AttributeError(msg)

    def __delattr__(self, key: str) -> NoReturn:
        msg = f'{self.__class__.__name__} is immutable'
        raise AttributeError(msg)

    def __getattr__(self, key: str) -> str:
        warnings.warn('The str interface for _CascadingStyleSheet objects is deprecated. Use css.filename instead.', RemovedInSphinx90Warning, stacklevel=2)
        return getattr(os.fspath(self.filename), key)

    def __getitem__(self, key: int | slice) -> str:
        warnings.warn('The str interface for _CascadingStyleSheet objects is deprecated. Use css.filename instead.', RemovedInSphinx90Warning, stacklevel=2)
        return os.fspath(self.filename)[key]

class _JavaScript:
    filename: str | os.PathLike[str]
    priority: int
    attributes: dict[str, str]

    def __init__(self, filename: str | os.PathLike[str], /, *, priority: int=500, **attributes: str) -> None:
        object.__setattr__(self, 'filename', filename)
        object.__setattr__(self, 'priority', priority)
        object.__setattr__(self, 'attributes', attributes)

    def __str__(self) -> str:
        attr = ''
        if self.attributes:
            attr = ', ' + ', '.join((f'{k}={v!r}' for k, v in self.attributes.items()))
        return f'{self.__class__.__name__}({self.filename!r}, priority={self.priority}{attr})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            warnings.warn('The str interface for _JavaScript objects is deprecated. Use js.filename instead.', RemovedInSphinx90Warning, stacklevel=2)
            return self.filename == other
        if not isinstance(other, _JavaScript):
            return NotImplemented
        return self.filename == other.filename and self.priority == other.priority and (self.attributes == other.attributes)

    def __hash__(self) -> int:
        return hash((self.filename, self.priority, *sorted(self.attributes.items())))

    def __setattr__(self, key: str, value: Any) -> NoReturn:
        msg = f'{self.__class__.__name__} is immutable'
        raise AttributeError(msg)

    def __delattr__(self, key: str) -> NoReturn:
        msg = f'{self.__class__.__name__} is immutable'
        raise AttributeError(msg)

    def __getattr__(self, key: str) -> str:
        warnings.warn('The str interface for _JavaScript objects is deprecated. Use js.filename instead.', RemovedInSphinx90Warning, stacklevel=2)
        return getattr(os.fspath(self.filename), key)

    def __getitem__(self, key: int | slice) -> str:
        warnings.warn('The str interface for _JavaScript objects is deprecated. Use js.filename instead.', RemovedInSphinx90Warning, stacklevel=2)
        return os.fspath(self.filename)[key]