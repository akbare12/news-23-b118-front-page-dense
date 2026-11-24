#!/usr/bin/env python3
"""news-23 b118 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
Validates the bundled PNG before copying: signature, IHDR 1024x1024, chunk CRCs.
"""
import hashlib
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MIN_BYTES = 10000
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error:", msg, file=sys.stderr)
    sys.exit(1)


def validate_png(data):
    """Validate the PNG structure; return (width, height)."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    if len(data) < 33:
        fail("PNG too short for IHDR")
    # First chunk must be IHDR, 13 bytes, with the expected dimensions.
    # Layout of the IHDR payload: width (4) + height (4) + bit depth (1) +
    # colour type (1) + compression (1) + filter (1) + interlace (1) = 13.
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        fail("first chunk is not a 13-byte IHDR")
    w, h, depth, ctype_code, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        fail("expected 1024x1024, got %dx%d" % (w, h))
    if depth != 8 or ctype_code not in (2, 6):
        fail("unexpected bit depth / colour type")
    if comp != 0 or filt != 0 or inter != 0:
        fail("unexpected compression / filter / interlace")
    crc_stored = struct.unpack(">I", data[29:33])[0]
    if zlib.crc32(data[12:29]) & 0xFFFFFFFF != crc_stored:
        fail("IHDR CRC mismatch")
    # Walk the remaining chunks: CRC each, require non-empty IDAT payload,
    # and an empty IEND as the final chunk with no trailing data.
    pos = 33
    idat_total = 0
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        cname = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            fail("truncated chunk %s" % cname.decode("latin-1", "replace"))
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if zlib.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF != crc_stored:
            fail("CRC mismatch in chunk %s" % cname.decode("latin-1", "replace"))
        if cname == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if cname == b"IEND":
            if clen != 0:
                fail("IEND must be empty")
            if pos + 12 != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            break
        pos += 12 + clen
    if not seen_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail("IDAT payload too small")
    return w, h


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir = os.path.abspath(out_dir)
    if out_dir == HERE or out_dir.startswith(HERE + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must be outside the repo")
    if os.path.exists(out_dir) and not os.path.isdir(out_dir):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    if not os.path.exists(SRC):
        fail("entry.png not found next to main.py")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) < MIN_BYTES:
        fail("entry.png too small (%d bytes)" % len(data))
    if len(data) > MAX_BYTES:
        fail("entry.png exceeds 1 MiB (%d bytes)" % len(data))
    validate_png(data)
    dst = os.path.join(out_dir, "entry.png")
    if os.path.abspath(dst) == SRC:
        fail("refusing to overwrite the source image")
    os.makedirs(out_dir, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        fail("output does not match source bytes")
    print("wrote %s (%d bytes, sha256 %s)"
          % (dst, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
