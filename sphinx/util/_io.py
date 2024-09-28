from __future__ import annotations
from typing import TYPE_CHECKING
from sphinx.util.console import strip_escape_sequences
if TYPE_CHECKING:
    from typing import Protocol

    class SupportsWrite(Protocol):
        pass

class TeeStripANSI:
    """File-like object writing to two streams."""

    def __init__(self, stream_term: SupportsWrite, stream_file: SupportsWrite) -> None:
        self.stream_term = stream_term
        self.stream_file = stream_file