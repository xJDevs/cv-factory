# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Utilities shared by the tests: extract text with several readers and compare."""
import re
import subprocess
import unicodedata
from collections import Counter
from functools import lru_cache
from pathlib import Path

from platform_tools import node_package, require

HERE = Path(__file__).resolve().parent
TEXT = {"capture_output": True, "text": True, "encoding": "utf-8", "errors": "replace"}


class Result:
    def __init__(self, number, name):
        self.number, self.name, self.failures, self.notes = number, name, [], []

    def fail(self, text):
        self.failures.append(text)

    def note(self, text):
        self.notes.append(text)

    @property
    def passed(self):
        return not self.failures


@lru_cache(maxsize=1)
def pdfjs_root():
    """pdfjs-dist from engine/.node first, then from the global npm folder."""
    local = node_package("pdfjs-dist")
    if local:
        return str(local)
    root = Path(subprocess.run([require("npm"), "root", "-g"], **TEXT).stdout.strip())
    return str(root / "pdfjs-dist")


@lru_cache(maxsize=1)
def tsx_command():
    """tsx from engine/.node first (run with node, the same on every system), otherwise through npx."""
    local = node_package("tsx")
    if local and (local / "dist" / "cli.mjs").is_file():
        return [require("node"), str(local / "dist" / "cli.mjs")]
    return [require("npx"), "--yes", "tsx"]


def with_pdftotext(pdf):
    return subprocess.run([require("pdftotext"), "-enc", "UTF-8", str(pdf), "-"], check=True, **TEXT).stdout


def with_pdfminer(pdf):
    from pdfminer.high_level import extract_text
    return extract_text(str(pdf))


def with_pdfjs(pdf):
    return subprocess.run([require("node"), str(HERE / "pdfjs_text.mjs"), str(pdf), pdfjs_root()],
                          check=True, **TEXT).stdout


def with_pdfium(pdf):
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(pdf))
    texts = [doc[i].get_textpage().get_text_range() for i in range(len(doc))]
    doc.close()
    return "\n".join(texts).replace("\r\n", "\n").replace("\r", "\n")


READERS = {"pdftotext": with_pdftotext, "pdfminer": with_pdfminer, "pdf.js": with_pdfjs,
           "pdfium": with_pdfium}


def extract_all(pdf):
    return {name: f(pdf) for name, f in READERS.items()}


def tokens(text):
    """Lowercase words, NFC. Ligatures (U+FB00–FB06) are NOT fixed: if they show up, the
    word does not match, which is exactly what would happen with a keyword search."""
    return re.findall(r"[^\W_]+", unicodedata.normalize("NFC", text).lower())


def recall(expected, extracted):
    """Percentage of the expected words (with repetitions) that appear in the extracted text."""
    wanted, found_tokens = Counter(tokens(expected)), Counter(tokens(extracted))
    total = sum(wanted.values())
    found = sum(min(n, found_tokens[t]) for t, n in wanted.items())
    missing = sorted(t for t, n in wanted.items() if found_tokens[t] < n)
    return (100.0 * found / total if total else 100.0), missing


def lines(text):
    return [re.sub(r"\s+", " ", l).strip() for l in text.splitlines() if l.strip()]


FORBIDDEN = [
    (r"\(cid:\d+\)", "(cid:N) code: character without a Unicode map"),
    ("[\\ufffd]", "U+FFFD: unrecognizable character"),
    ("[\\ue000-\\uf8ff]", "private use (icons, Word's Symbol bullet)"),
    ("[\\U000f0000-\\U0010ffff]", "supplementary private use"),
    ("[\\U0001f000-\\U0001faff]", "emoji or pictograph"),
    ("[\\u2600-\\u27bf\\u25a0-\\u25ff]", "decorative symbol (stars, check marks, boxes, arrows)"),
    ("[\\u200b-\\u200f\\u2060\\ufeff\\u00ad]", "invisible character or soft hyphen"),
    ("[\\ufb00-\\ufb06]", "ligature (fi, fl, ff...)"),
    ("[\\u0300-\\u036f]", "loose (combining) accent"),
    ("[\\x00-\\x08\\x0b\\x0e-\\x1f\\x7f-\\x9f]", "control character"),
]


def forbidden_chars(text):
    """Returns a list of (description, examples) found."""
    t = unicodedata.normalize("NFC", text)
    found = []
    for pattern, desc in FORBIDDEN:
        m = re.findall(pattern, t)
        if m:
            ex = sorted({x if len(x) > 1 else f"U+{ord(x):04X}" for x in m})[:6]
            found.append((desc, " ".join(ex)))
    return found
