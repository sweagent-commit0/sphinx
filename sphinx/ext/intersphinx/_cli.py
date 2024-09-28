"""This module provides contains the code for intersphinx command-line utilities."""
from __future__ import annotations
import sys
from sphinx.ext.intersphinx._load import _fetch_inventory

def inspect_main(argv: list[str], /) -> int:
    """Debug functionality to print out an inventory"""
    pass