"""This module contains the code for loading intersphinx inventories."""
from __future__ import annotations
import concurrent.futures
import functools
import posixpath
import time
from operator import itemgetter
from os import path
from typing import TYPE_CHECKING
from urllib.parse import urlsplit, urlunsplit
from sphinx.builders.html import INVENTORY_FILENAME
from sphinx.errors import ConfigError
from sphinx.ext.intersphinx._shared import LOGGER, InventoryAdapter, _IntersphinxProject
from sphinx.locale import __
from sphinx.util import requests
from sphinx.util.inventory import InventoryFile
if TYPE_CHECKING:
    from pathlib import Path
    from typing import IO
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.ext.intersphinx._shared import IntersphinxMapping, InventoryCacheEntry, InventoryLocation, InventoryName, InventoryURI
    from sphinx.util.typing import Inventory

def validate_intersphinx_mapping(app: Sphinx, config: Config) -> None:
    """Validate and normalise :confval:`intersphinx_mapping`.

    Ensure that:

    * Keys are non-empty strings.
    * Values are two-element tuples or lists.
    * The first element of each value pair (the target URI)
      is a non-empty string.
    * The second element of each value pair (inventory locations)
      is a tuple of non-empty strings or None.
    """
    pass

def load_mappings(app: Sphinx) -> None:
    """Load all intersphinx mappings into the environment.

    The intersphinx mappings are expected to be normalized.
    """
    pass

def fetch_inventory(app: Sphinx, uri: InventoryURI, inv: str) -> Inventory:
    """Fetch, parse and return an intersphinx inventory file."""
    pass

def _fetch_inventory(*, target_uri: InventoryURI, inv_location: str, config: Config, srcdir: Path) -> Inventory:
    """Fetch, parse and return an intersphinx inventory file."""
    pass

def _get_safe_url(url: str) -> str:
    """Gets version of *url* with basic auth passwords obscured. This function
    returns results suitable for printing and logging.

    E.g.: https://user:12345@example.com => https://user@example.com

    :param url: a url
    :type url: ``str``

    :return: *url* with password removed
    :rtype: ``str``
    """
    pass

def _strip_basic_auth(url: str) -> str:
    """Returns *url* with basic auth credentials removed. Also returns the
    basic auth username and password if they're present in *url*.

    E.g.: https://user:pass@example.com => https://example.com

    *url* need not include basic auth credentials.

    :param url: url which may or may not contain basic auth credentials
    :type url: ``str``

    :return: *url* with any basic auth creds removed
    :rtype: ``str``
    """
    pass

def _read_from_url(url: str, *, config: Config) -> IO:
    """Reads data from *url* with an HTTP *GET*.

    This function supports fetching from resources which use basic HTTP auth as
    laid out by RFC1738 § 3.1. See § 5 for grammar definitions for URLs.

    .. seealso:

       https://www.ietf.org/rfc/rfc1738.txt

    :param url: URL of an HTTP resource
    :type url: ``str``

    :return: data read from resource described by *url*
    :rtype: ``file``-like object
    """
    pass