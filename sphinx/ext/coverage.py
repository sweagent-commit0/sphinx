"""Check Python modules and C API for coverage.

Mostly written by Josip Dzolonga for the Google Highly Open Participation
contest.
"""
from __future__ import annotations
import glob
import inspect
import pickle
import pkgutil
import re
import sys
from importlib import import_module
from os import path
from typing import IO, TYPE_CHECKING, Any, TextIO
import sphinx
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.console import red
from sphinx.util.inspect import safe_getattr
if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator, Sequence, Set
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)

def _load_modules(mod_name: str, ignored_module_exps: Iterable[re.Pattern[str]]) -> Set[str]:
    """Recursively load all submodules.

    :param mod_name: The name of a module to load submodules for.
    :param ignored_module_exps: A list of regexes for modules to ignore.
    :returns: A set of modules names including the provided module name,
        ``mod_name``
    :raises ImportError: If the module indicated by ``mod_name`` could not be
        loaded.
    """
    pass

def _determine_py_coverage_modules(coverage_modules: Sequence[str], seen_modules: Set[str], ignored_module_exps: Iterable[re.Pattern[str]], py_undoc: dict[str, dict[str, Any]]) -> list[str]:
    """Return a sorted list of modules to check for coverage.

    Figure out which of the two operating modes to use:

    - If 'coverage_modules' is not specified, we check coverage for all modules
      seen in the documentation tree. Any objects found in these modules that are
      not documented will be noted. This will therefore only identify missing
      objects, but it requires no additional configuration.

    - If 'coverage_modules' is specified, we check coverage for all modules
      specified in this configuration value. Any objects found in these modules
      that are not documented will be noted. In addition, any objects from other
      modules that are documented will be noted. This will therefore identify both
      missing modules and missing objects, but it requires manual configuration.
    """
    pass

class CoverageBuilder(Builder):
    """
    Evaluates coverage of code in the documentation.
    """
    name = 'coverage'
    epilog = __('Testing of coverage in the sources finished, look at the results in %(outdir)s' + path.sep + 'python.txt.')

    def _write_py_statistics(self, op: TextIO) -> None:
        """Outputs the table of ``op``."""
        pass