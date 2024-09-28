"""Glue code for the jinja2 templating engine."""
from __future__ import annotations
import os
from os import path
from pprint import pformat
from typing import TYPE_CHECKING, Any
from jinja2 import BaseLoader, FileSystemLoader, TemplateNotFound
from jinja2.sandbox import SandboxedEnvironment
from jinja2.utils import open_if_exists, pass_context
from sphinx.application import TemplateBridge
from sphinx.util import logging
from sphinx.util.osutil import _last_modified_time
if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from jinja2.environment import Environment
    from sphinx.builders import Builder
    from sphinx.theming import Theme

def _todim(val: int | str) -> str:
    """
    Make val a css dimension. In particular the following transformations
    are performed:

    - None -> 'initial' (default CSS value)
    - 0 -> '0'
    - ints and string representations of ints are interpreted as pixels.

    Everything else is returned unchanged.
    """
    pass

def accesskey(context: Any, key: str) -> str:
    """Helper to output each access key only once."""
    pass

class idgen:

    def __init__(self) -> None:
        self.id = 0

    def __next__(self) -> int:
        self.id += 1
        return self.id
    next = __next__

class SphinxFileSystemLoader(FileSystemLoader):
    """
    FileSystemLoader subclass that is not so strict about '..'  entries in
    template names.
    """

class BuiltinTemplateLoader(TemplateBridge, BaseLoader):
    """
    Interfaces the rendering environment of jinja2 for use in Sphinx.
    """