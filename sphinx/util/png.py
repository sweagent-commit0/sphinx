"""PNG image manipulation helpers."""
from __future__ import annotations
import binascii
import struct
LEN_IEND = 12
LEN_DEPTH = 22
DEPTH_CHUNK_LEN = struct.pack('!i', 10)
DEPTH_CHUNK_START = b'tEXtDepth\x00'
IEND_CHUNK = b'\x00\x00\x00\x00IEND\xaeB`\x82'

def read_png_depth(filename: str) -> int | None:
    """Read the special tEXt chunk indicating the depth from a PNG file."""
    pass

def write_png_depth(filename: str, depth: int) -> None:
    """Write the special tEXt chunk indicating the depth to a PNG file.

    The chunk is placed immediately before the special IEND chunk.
    """
    pass