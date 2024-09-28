from __future__ import annotations
import os
import shutil
import sys
import warnings
from typing import IO, TYPE_CHECKING, Any
from sphinx.deprecation import RemovedInSphinx90Warning
if TYPE_CHECKING:
    import builtins
    from collections.abc import Callable
warnings.warn("'sphinx.testing.path' is deprecated. Use 'os.path' or 'pathlib' instead.", RemovedInSphinx90Warning, stacklevel=2)
FILESYSTEMENCODING = sys.getfilesystemencoding() or sys.getdefaultencoding()

def getumask() -> int:
    """Get current umask value"""
    pass
UMASK = getumask()

class path(str):
    """
    Represents a path which behaves like a string.
    """
    __slots__ = ()

    @property
    def parent(self) -> path:
        """
        The name of the directory the file or directory is in.
        """
        pass

    def abspath(self) -> path:
        """
        Returns the absolute path.
        """
        pass

    def isabs(self) -> bool:
        """
        Returns ``True`` if the path is absolute.
        """
        pass

    def isdir(self) -> bool:
        """
        Returns ``True`` if the path is a directory.
        """
        pass

    def isfile(self) -> bool:
        """
        Returns ``True`` if the path is a file.
        """
        pass

    def islink(self) -> bool:
        """
        Returns ``True`` if the path is a symbolic link.
        """
        pass

    def ismount(self) -> bool:
        """
        Returns ``True`` if the path is a mount point.
        """
        pass

    def rmtree(self, ignore_errors: bool=False, onerror: Callable[[Callable[..., Any], str, Any], object] | None=None) -> None:
        """
        Removes the file or directory and any files or directories it may
        contain.

        :param ignore_errors:
            If ``True`` errors are silently ignored, otherwise an exception
            is raised in case an error occurs.

        :param onerror:
            A callback which gets called with the arguments `func`, `path` and
            `exc_info`. `func` is one of :func:`os.listdir`, :func:`os.remove`
            or :func:`os.rmdir`. `path` is the argument to the function which
            caused it to fail and `exc_info` is a tuple as returned by
            :func:`sys.exc_info`.
        """
        pass

    def copytree(self, destination: str, symlinks: bool=False) -> None:
        """
        Recursively copy a directory to the given `destination`. If the given
        `destination` does not exist it will be created.

        :param symlinks:
            If ``True`` symbolic links in the source tree result in symbolic
            links in the destination tree otherwise the contents of the files
            pointed to by the symbolic links are copied.
        """
        pass

    def movetree(self, destination: str) -> None:
        """
        Recursively move the file or directory to the given `destination`
        similar to the  Unix "mv" command.

        If the `destination` is a file it may be overwritten depending on the
        :func:`os.rename` semantics.
        """
        pass
    move = movetree

    def unlink(self) -> None:
        """
        Removes a file.
        """
        pass

    def stat(self) -> Any:
        """
        Returns a stat of the file.
        """
        pass

    def write_text(self, text: str, encoding: str='utf-8', **kwargs: Any) -> None:
        """
        Writes the given `text` to the file.
        """
        pass

    def read_text(self, encoding: str='utf-8', **kwargs: Any) -> str:
        """
        Returns the text in the file.
        """
        pass

    def read_bytes(self) -> builtins.bytes:
        """
        Returns the bytes in the file.
        """
        pass

    def write_bytes(self, bytes: bytes, append: bool=False) -> None:
        """
        Writes the given `bytes` to the file.

        :param append:
            If ``True`` given `bytes` are added at the end of the file.
        """
        pass

    def exists(self) -> bool:
        """
        Returns ``True`` if the path exist.
        """
        pass

    def lexists(self) -> bool:
        """
        Returns ``True`` if the path exists unless it is a broken symbolic
        link.
        """
        pass

    def makedirs(self, mode: int=511, exist_ok: bool=False) -> None:
        """
        Recursively create directories.
        """
        pass

    def joinpath(self, *args: Any) -> path:
        """
        Joins the path with the argument given and returns the result.
        """
        pass
    __div__ = __truediv__ = joinpath

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__repr__()})'