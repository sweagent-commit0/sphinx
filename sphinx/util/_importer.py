from __future__ import annotations
from importlib import import_module
from typing import Any
from sphinx.errors import ExtensionError

def import_object(object_name: str, /, source: str='') -> Any:
    """Import python object by qualname."""
    pass