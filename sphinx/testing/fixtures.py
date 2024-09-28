"""Sphinx test fixtures for pytest"""
from __future__ import annotations
import shutil
import subprocess
import sys
from collections import namedtuple
from io import StringIO
from typing import TYPE_CHECKING
import pytest
from sphinx.testing.util import SphinxTestApp, SphinxTestAppWrapperForSkipBuilding
if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from pathlib import Path
    from typing import Any
DEFAULT_ENABLED_MARKERS = ['sphinx(buildername="html", *, testroot="root", srcdir=None, confoverrides=None, freshenv=False, warningiserror=False, tags=None, verbosity=0, parallel=0, builddir=None, docutils_conf=None): arguments to initialize the sphinx test application.', 'test_params(shared_result=...): test parameters.']

def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers"""
    pass

class SharedResult:
    cache: dict[str, dict[str, str]] = {}

@pytest.fixture
def app_params(request: Any, test_params: dict[str, Any], shared_result: SharedResult, sphinx_test_tempdir: str, rootdir: Path) -> _app_params:
    """
    Parameters that are specified by 'pytest.mark.sphinx' for
    sphinx.application.Sphinx initialization
    """
    pass
_app_params = namedtuple('_app_params', 'args,kwargs')

@pytest.fixture
def test_params(request: Any) -> dict[str, Any]:
    """
    Test parameters that are specified by 'pytest.mark.test_params'

    :param Union[str] shared_result:
       If the value is provided, app._status and app._warning objects will be
       shared in the parametrized test functions and/or test functions that
       have same 'shared_result' value.
       **NOTE**: You can not specify both shared_result and srcdir.
    """
    pass

@pytest.fixture
def app(test_params: dict[str, Any], app_params: _app_params, make_app: Callable[[], SphinxTestApp], shared_result: SharedResult) -> Iterator[SphinxTestApp]:
    """
    Provides the 'sphinx.application.Sphinx' object
    """
    pass

@pytest.fixture
def status(app: SphinxTestApp) -> StringIO:
    """
    Back-compatibility for testing with previous @with_app decorator
    """
    pass

@pytest.fixture
def warning(app: SphinxTestApp) -> StringIO:
    """
    Back-compatibility for testing with previous @with_app decorator
    """
    pass

@pytest.fixture
def make_app(test_params: dict[str, Any]) -> Iterator[Callable[[], SphinxTestApp]]:
    """
    Provides make_app function to initialize SphinxTestApp instance.
    if you want to initialize 'app' in your test function. please use this
    instead of using SphinxTestApp class directory.
    """
    pass

@pytest.fixture
def if_graphviz_found(app: SphinxTestApp) -> None:
    """
    The test will be skipped when using 'if_graphviz_found' fixture and graphviz
    dot command is not found.
    """
    pass

@pytest.fixture(scope='session')
def sphinx_test_tempdir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Temporary directory."""
    pass

@pytest.fixture
def rollback_sysmodules() -> Iterator[None]:
    """
    Rollback sys.modules to its value before testing to unload modules
    during tests.

    For example, used in test_ext_autosummary.py to permit unloading the
    target module to clear its cache.
    """
    pass