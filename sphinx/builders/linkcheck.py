"""The CheckExternalLinksBuilder class."""
from __future__ import annotations
import contextlib
import json
import re
import socket
import time
from html.parser import HTMLParser
from os import path
from queue import PriorityQueue, Queue
from threading import Thread
from typing import TYPE_CHECKING, NamedTuple, cast
from urllib.parse import quote, unquote, urlparse, urlsplit, urlunparse
from docutils import nodes
from requests.exceptions import ConnectionError, HTTPError, SSLError, TooManyRedirects
from requests.exceptions import Timeout as RequestTimeout
from sphinx.builders.dummy import DummyBuilder
from sphinx.locale import __
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import encode_uri, logging, requests
from sphinx.util.console import darkgray, darkgreen, purple, red, turquoise
from sphinx.util.http_date import rfc1123_to_epoch
from sphinx.util.nodes import get_node_line
if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from typing import Any
    from requests import Response
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.util._pathlib import _StrPath
    from sphinx.util.typing import ExtensionMetadata
logger = logging.getLogger(__name__)
uri_re = re.compile('([a-z]+:)?//')
DEFAULT_REQUEST_HEADERS = {'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8'}
CHECK_IMMEDIATELY = 0
QUEUE_POLL_SECS = 1
DEFAULT_DELAY = 60.0

class CheckExternalLinksBuilder(DummyBuilder):
    """
    Checks for broken external links.
    """
    name = 'linkcheck'
    epilog = __('Look for any errors in the above output or in %(outdir)s/output.txt')

class HyperlinkCollector(SphinxPostTransform):
    builders = ('linkcheck',)
    default_priority = 800

    def find_uri(self, node: nodes.Element) -> str | None:
        """Find a URI for a given node.

        This call can be used to retrieve a URI from a provided node. If no
        URI exists for a provided node, this call will return ``None``.

        This method can be useful for extension developers who wish to
        easily inject hyperlinks into a builder by only needing to override
        this method.

        :param node: A node class
        :returns: URI of the node
        """
        pass

    def _add_uri(self, uri: str, node: nodes.Element) -> None:
        """Registers a node's URI into a builder's collection of hyperlinks.

        Provides the ability to register a URI value determined from a node
        into the linkcheck's builder. URI's processed through this call can
        be manipulated through a ``linkcheck-process-uri`` event before the
        builder attempts to validate.

        :param uri: URI to add
        :param node: A node class where the URI was found
        """
        pass

class Hyperlink(NamedTuple):
    uri: str
    docname: str
    docpath: _StrPath
    lineno: int

class HyperlinkAvailabilityChecker:

    def __init__(self, config: Config) -> None:
        self.config = config
        self.rate_limits: dict[str, RateLimit] = {}
        self.rqueue: Queue[CheckResult] = Queue()
        self.workers: list[Thread] = []
        self.wqueue: PriorityQueue[CheckRequest] = PriorityQueue()
        self.num_workers: int = config.linkcheck_workers
        self.to_ignore: list[re.Pattern[str]] = list(map(re.compile, self.config.linkcheck_ignore))

class CheckRequest(NamedTuple):
    next_check: float
    hyperlink: Hyperlink | None

class CheckResult(NamedTuple):
    uri: str
    docname: str
    lineno: int
    status: str
    message: str
    code: int

class HyperlinkAvailabilityCheckWorker(Thread):
    """A worker class for checking the availability of hyperlinks."""

    def __init__(self, config: Config, rqueue: Queue[CheckResult], wqueue: Queue[CheckRequest], rate_limits: dict[str, RateLimit]) -> None:
        self.rate_limits = rate_limits
        self.rqueue = rqueue
        self.wqueue = wqueue
        self.anchors_ignore: list[re.Pattern[str]] = list(map(re.compile, config.linkcheck_anchors_ignore))
        self.anchors_ignore_for_url: list[re.Pattern[str]] = list(map(re.compile, config.linkcheck_anchors_ignore_for_url))
        self.documents_exclude: list[re.Pattern[str]] = list(map(re.compile, config.linkcheck_exclude_documents))
        self.auth = [(re.compile(pattern), auth_info) for pattern, auth_info in config.linkcheck_auth]
        self.timeout: int | float | None = config.linkcheck_timeout
        self.request_headers: dict[str, dict[str, str]] = config.linkcheck_request_headers
        self.check_anchors: bool = config.linkcheck_anchors
        self.allowed_redirects: dict[re.Pattern[str], re.Pattern[str]]
        self.allowed_redirects = config.linkcheck_allowed_redirects
        self.retries: int = config.linkcheck_retries
        self.rate_limit_timeout = config.linkcheck_rate_limit_timeout
        self._allow_unauthorized = config.linkcheck_allow_unauthorized
        if config.linkcheck_report_timeouts_as_broken:
            self._timeout_status = 'broken'
        else:
            self._timeout_status = 'timeout'
        self.user_agent = config.user_agent
        self.tls_verify = config.tls_verify
        self.tls_cacerts = config.tls_cacerts
        self._session = requests._Session()
        super().__init__(daemon=True)

def contains_anchor(response: Response, anchor: str) -> bool:
    """Determine if an anchor is contained within an HTTP response."""
    pass

class AnchorCheckParser(HTMLParser):
    """Specialised HTML parser that looks for a specific anchor."""

    def __init__(self, search_anchor: str) -> None:
        super().__init__()
        self.search_anchor = search_anchor
        self.found = False

class RateLimit(NamedTuple):
    delay: float
    next_check: float

def rewrite_github_anchor(app: Sphinx, uri: str) -> str | None:
    """Rewrite anchor name of the hyperlink to github.com

    The hyperlink anchors in github.com are dynamically generated.  This rewrites
    them before checking and makes them comparable.
    """
    pass

def compile_linkcheck_allowed_redirects(app: Sphinx, config: Config) -> None:
    """Compile patterns in linkcheck_allowed_redirects to the regexp objects."""
    pass