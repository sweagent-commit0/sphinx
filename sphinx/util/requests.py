"""Simple requests package loader"""
from __future__ import annotations
import warnings
from typing import Any
from urllib.parse import urlsplit
import requests
from urllib3.exceptions import InsecureRequestWarning
import sphinx
_USER_AGENT = f'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0 Sphinx/{sphinx.__version__}'

def _get_tls_cacert(url: str, certs: str | dict[str, str] | None) -> str | bool:
    """Get additional CA cert for a specific URL."""
    pass

def get(url: str, **kwargs: Any) -> requests.Response:
    """Sends a GET request like ``requests.get()``.

    This sets up User-Agent header and TLS verification automatically.
    """
    pass

def head(url: str, **kwargs: Any) -> requests.Response:
    """Sends a HEAD request like ``requests.head()``.

    This sets up User-Agent header and TLS verification automatically.
    """
    pass

class _Session(requests.Session):

    def request(self, method: str, url: str, _user_agent: str='', _tls_info: tuple[bool, str | dict[str, str] | None]=(), **kwargs: Any) -> requests.Response:
        """Sends a request with an HTTP verb and url.

        This sets up User-Agent header and TLS verification automatically.
        """
        pass