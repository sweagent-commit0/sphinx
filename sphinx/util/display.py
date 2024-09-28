from __future__ import annotations
import functools
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.console import bold, color_terminal
if False:
    from collections.abc import Callable, Iterable, Iterator
    from types import TracebackType
    from typing import Any, TypeVar
    from typing_extensions import ParamSpec
    T = TypeVar('T')
    P = ParamSpec('P')
    R = TypeVar('R')
logger = logging.getLogger(__name__)

class SkipProgressMessage(Exception):
    pass

class progress_message:

    def __init__(self, message: str, *, nonl: bool=True) -> None:
        self.message = message
        self.nonl = nonl

    def __enter__(self) -> None:
        logger.info(bold(self.message + '... '), nonl=self.nonl)

    def __exit__(self, typ: type[BaseException] | None, val: BaseException | None, tb: TracebackType | None) -> bool:
        prefix = '' if self.nonl else bold(self.message + ': ')
        if isinstance(val, SkipProgressMessage):
            logger.info(prefix + __('skipped'))
            if val.args:
                logger.info(*val.args)
            return True
        elif val:
            logger.info(prefix + __('failed'))
        else:
            logger.info(prefix + __('done'))
        return False

    def __call__(self, f: Callable[P, R]) -> Callable[P, R]:

        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with self:
                return f(*args, **kwargs)
        return wrapper