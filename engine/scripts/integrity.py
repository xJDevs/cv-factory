# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Integrity check of the engine's core files against the original release.

Usage:
  python3 integrity.py --write   writes engine/MANIFEST.sha256 (sha256 of every engine file)
  python3 integrity.py --check   compares the engine files with MANIFEST.sha256

--check only warns: it always exits with code 0, so it never blocks anything.
Left out of the manifest: .venv/, .node/, __pycache__/, *.pyc, .DS_Store, example/output/
and MANIFEST.sha256 itself.

Paths are always written with "/" (also on Windows). Text files are hashed with their line
endings turned into LF, so a checkout that writes CRLF (Git on Windows with autocrlf) still
matches; binary files (fonts, PDF, DOCX, images, workbooks) are hashed byte for byte.
"""
import argparse
import hashlib
import sys
from pathlib import Path

import platform_tools

ENGINE = Path(__file__).resolve().parent.parent
MANIFEST = ENGINE / "MANIFEST.sha256"
SKIP_DIRS = {".venv", ".node", "__pycache__"}
SKIP_PREFIXES = ("example/output/",)
SKIP_FILES = {".DS_Store", "MANIFEST.sha256"}
BINARY = {".ttf", ".otf", ".woff", ".woff2", ".pdf", ".docx", ".xlsx", ".png", ".jpg", ".jpeg", ".zip"}


def included(rel):
    parts = rel.split("/")
    if any(p in SKIP_DIRS for p in parts[:-1]):
        return False
    if parts[-1] in SKIP_FILES or parts[-1].endswith(".pyc"):
        return False
    return not any(rel.startswith(p) for p in SKIP_PREFIXES)


def sha256(path):
    data = Path(path).read_bytes()
    if Path(path).suffix.lower() not in BINARY:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def current():
    files = {}
    for p in ENGINE.rglob("*"):
        if p.is_file() and not p.is_symlink():
            rel = p.relative_to(ENGINE).as_posix()
            if included(rel):
                files[rel] = sha256(p)
    return dict(sorted(files.items()))


def read_manifest():
    out = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, rel = line.split(None, 1)
            out[rel.strip()] = digest
    return out


def write():
    files = current()
    MANIFEST.write_text("".join(f"{d}  {rel}\n" for rel, d in files.items()), encoding="utf-8", newline="\n")
    print(f"Integrity: wrote {MANIFEST.name} with {len(files)} files.")


def check():
    if not MANIFEST.exists():
        print(f"WARNING: {MANIFEST.name} was not found, so the core files cannot be compared with the original release.")
        return
    expected, now = read_manifest(), current()
    modified = sorted(r for r in expected if r in now and now[r] != expected[r])
    deleted = sorted(r for r in expected if r not in now)
    added = sorted(r for r in now if r not in expected)
    if not (modified or deleted or added):
        print("Integrity: all core files match the original release.")
        return
    print("WARNING: core files were changed since the original release.")
    for title, items in (("Modified", modified), ("Added", added), ("Deleted", deleted)):
        for rel in items:
            print(f"  {title}: {rel}")
    print("CVs may fail the tests because of these changes. If that happens, "
          "restore the original files from the release.")


def main():
    ap = argparse.ArgumentParser(description="Check the engine's core files against the original release.")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="write MANIFEST.sha256")
    group.add_argument("--check", action="store_true", help="compare with MANIFEST.sha256 (warns only)")
    a = ap.parse_args()
    write() if a.write else check()
    return 0


if __name__ == "__main__":
    platform_tools.utf8_console()
    sys.exit(main())
