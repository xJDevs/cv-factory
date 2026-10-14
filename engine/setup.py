# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Gets a local machine (macOS, Linux or Windows) ready to run the CV engine.

Usage, with the system Python 3.10 or newer, from the project folder:
  macOS / Linux:  python3 engine/setup.py
  Windows:        py engine\\setup.py     (or: python engine\\setup.py)

Standard library only. Installs only what is missing, all inside engine/ (.venv for Python,
.node for Node), and ends with "READY" (exit code 0) or "NOT READY: ..." (exit code 1).
The line before READY says how to run the engine on this machine.
"""
import os
import subprocess
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE / "scripts"))
import platform_tools as pt  # noqa: E402

MIN_PYTHON = (3, 10)
PACKAGES = [("jinja2", "jinja2==3.1.6"), ("pikepdf", "pikepdf==10.5.1"), ("docx", "python-docx==1.2.0"),
            ("pdfminer", "pdfminer.six==20251230"), ("pypdfium2", "pypdfium2==5.7.1"),
            ("playwright", "playwright==1.56.0"), ("openpyxl", "openpyxl==3.1.5")]
NODE_PACKAGES = [("pdfjs-dist", "pdfjs-dist@5.7.284"), ("tsx", "tsx@4.21.0")]
PROGRAMS = ["pdftotext", "pdffonts", "soffice", "node", "npx", "git"]
PREINSTALLED_BROWSERS = Path("/opt/pw-browsers")
CHROMIUM_CHECK = ("from playwright.sync_api import sync_playwright\n"
                  "with sync_playwright() as p:\n"
                  "    p.chromium.launch().close()\n")
VERSION_CHECK = f"import sys; sys.exit(sys.version_info < {MIN_PYTHON})"
QUIET = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}


def run(cmd, **kwargs):
    """Runs a command; False (instead of an exception) if it fails or cannot start."""
    try:
        return subprocess.run([str(c) for c in cmd], **kwargs).returncode == 0
    except OSError:
        return False


def python_section(py):
    print("== Python (engine/.venv) ==")
    missing = False
    if py.exists() and not run([py, "-c", VERSION_CHECK], **QUIET):
        print(f"recreating {pt.VENV} (its Python is older than {'.'.join(map(str, MIN_PYTHON))})")
        if not run([sys.executable, "-m", "venv", "--clear", pt.VENV]) or not py.exists():
            print(f"MISSING python venv (install hint: {pt.hint('python')})")
            return True
    if not py.exists():
        print(f"creating {pt.VENV}")
        if not run([sys.executable, "-m", "venv", pt.VENV]) or not py.exists():
            print(f"MISSING python venv (install hint: {pt.hint('python')})")
            return True
    for module, package in PACKAGES:
        if run([py, "-c", f"import {module}"], **QUIET):
            print(f"ok  {module}")
        else:
            print(f"installing {package}")
            if not run([py, "-m", "pip", "install", "-q", "--disable-pip-version-check", package]):
                print(f"MISSING {package}")
                missing = True
    return missing


def chromium_section(py):
    print("== Chromium (for the PDF) ==")
    ok = lambda: py.exists() and run([py, "-c", CHROMIUM_CHECK], **QUIET)  # noqa: E731
    if ok():
        print("ok  chromium")
        return False
    if PREINSTALLED_BROWSERS.is_dir():
        print(f"MISSING chromium (this environment has preinstalled browsers in {PREINSTALLED_BROWSERS}: "
              "do not run 'playwright install')")
        return True
    if not py.exists():
        print("MISSING chromium (needs the Python environment first)")
        return True
    print("installing chromium (playwright)")
    if run([py, "-m", "playwright", "install", "chromium"]) and ok():
        print("ok  chromium")
        return False
    print(f"MISSING chromium (try: {py} -m playwright install chromium)")
    return True


def programs_section():
    print("== System programs ==")
    missing = False
    for program in PROGRAMS:
        found = pt.find(program)
        if found:
            print(f"ok  {program}" + ("" if Path(found).parent in path_folders() else f"  ({found})"))
        else:
            extra = f"; or set {pt.POPPLER_ENV} to its folder" if program in pt.POPPLER else ""
            print(f"MISSING {program} (install hint: {pt.hint(program)}{extra})")
            missing = True
    return missing


def path_folders():
    return {Path(p) for p in os.environ.get("PATH", "").split(os.pathsep) if p}


def node_section():
    print("== Node (pdf.js and tsx for tests 2 and 5, in engine/.node) ==")
    missing = False
    npm = pt.find("npm")
    for name, package in NODE_PACKAGES:
        if pt.node_package(name):
            print(f"ok  {name}")
        elif npm:
            print(f"installing {package}")
            if not run([npm, "install", "-g", "--prefix", pt.LOCAL_NODE, "--silent", package]) \
                    or not pt.node_package(name):
                print(f"MISSING {package}")
                missing = True
        else:
            print(f"MISSING {package} (needs npm: {pt.hint('node')})")
            missing = True
    return missing


def fonts_section():
    print("== Fonts ==")
    if (ENGINE / "fonts" / "Carlito-Regular.ttf").is_file():
        print("ok  Carlito")
        return False
    print("MISSING fonts/Carlito-*.ttf")
    return True


def reader_section():
    """pdftotext builds differ: some (e.g. Chocolatey's poppler on Windows) join every line of a block,
    so section titles end up glued to the next paragraph and tests 4 and 8 can never pass. Check the
    installed one on the shipped example before anything else depends on it."""
    print("== PDF reader self-check ==")
    exe = pt.find("pdftotext")
    pdf = ENGINE / "example" / "output" / "Ana-Maria-Solis-Vargas-Resume.pdf"
    if not exe or not pdf.is_file():
        print("skipped (pdftotext or the example PDF is missing)")
        return False
    try:
        out = subprocess.run([exe, "-enc", "UTF-8", str(pdf), "-"], capture_output=True, check=True,
                             encoding="utf-8", errors="replace").stdout
    except (OSError, subprocess.SubprocessError) as e:
        print(f"MISSING a working pdftotext ({e})")
        return True
    if any(line.strip() == "PROFESSIONAL SUMMARY" for line in out.splitlines()):
        print(f"ok  pdftotext keeps section titles on their own line ({exe})")
        return False
    print(f"MISSING a compatible pdftotext: {exe} joins section titles with the next paragraph, so "
          f"tests 4 and 8 would always fail. Install the poppler-windows build instead "
          f"({pt.hint('pdftotext')}) and, if both are installed, set CVF_POPPLER_BIN to its folder.")
    return True


def integrity_section(py):
    print("== Integrity ==")
    sys.stdout.flush()
    run([py if py.exists() else sys.executable, ENGINE / "scripts" / "integrity.py", "--check"])


def how_to_run(py):
    """The command prefix for this machine, relative to the project folder (the parent of engine/)."""
    rel = py.relative_to(ENGINE.parent)
    script = Path("engine") / "scripts" / "cv.py"
    return f"Run the engine with: {rel} {script} ...   (full path: {py})"


def main():
    pt.utf8_console()
    os.environ["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"   # no "a new release of pip is available" notice
    if sys.version_info < MIN_PYTHON:
        print(f"MISSING Python {'.'.join(map(str, MIN_PYTHON))} or newer (this is {sys.version.split()[0]}; "
              f"install hint: {pt.hint('python')})")
        print("NOT READY: check the items marked MISSING")
        return 1
    py = pt.venv_python()
    missing = python_section(py)
    missing |= chromium_section(py)
    missing |= programs_section()
    missing |= node_section()
    missing |= fonts_section()
    missing |= reader_section()
    integrity_section(py)
    sys.stdout.flush()
    if missing:
        print("NOT READY: check the items marked MISSING")
        return 1
    print(how_to_run(py))
    print("READY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
