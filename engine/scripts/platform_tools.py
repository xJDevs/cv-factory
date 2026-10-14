# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Finds the programs and local folders the engine uses, the same way on macOS, Linux and Windows.

Standard library only: setup.py imports it with the system Python, before engine/.venv exists.

- find("pdftotext") returns the full path of a program, or None. It looks, in order: in the
  folder of the CVF_POPPLER_BIN environment variable (poppler programs only), in PATH, and in
  the usual install folders of each system (LibreOffice is never in PATH on Windows, and a
  program installed a minute ago is not in the PATH of an agent that was already open).
- require("pdftotext") is the same, but raises MissingProgram (an OSError) with an install hint.
- On Windows, npm and npx are .cmd files: find() returns the full path, so subprocess can run
  them without a shell.
- venv_python(): engine/.venv/bin/python (macOS, Linux) or engine\\.venv\\Scripts\\python.exe (Windows).
- node_package("tsx"): engine/.node/lib/node_modules/tsx (macOS, Linux) or
  engine\\.node\\node_modules\\tsx (Windows), the two layouts of "npm install -g --prefix".
- cache_dir(): $XDG_CACHE_HOME, otherwise %LOCALAPPDATA% on Windows, otherwise ~/.cache.
- utf8_console(): the report uses ✅/❌; a Windows console or pipe would otherwise use cp1252.
"""
import glob
import os
import shutil
import sys
from pathlib import Path

WINDOWS = os.name == "nt"
MAC = sys.platform == "darwin"
ENGINE = Path(__file__).resolve().parent.parent
VENV = ENGINE / ".venv"
LOCAL_NODE = ENGINE / ".node"  # created by setup.py (npm install -g --prefix engine/.node)
POPPLER = ("pdftotext", "pdffonts", "pdftoppm")
POPPLER_ENV = "CVF_POPPLER_BIN"

# How to install each program, per system (Windows: winget package IDs).
HINTS = {
    "mac": {
        "poppler": "brew install poppler",
        "soffice": "brew install --cask libreoffice",
        "node": "brew install node",
        "git": "xcode-select --install  (or: brew install git)",
        "python": "brew install python",
    },
    "linux": {
        "poppler": "sudo apt install poppler-utils",
        "soffice": "sudo apt install libreoffice-writer fonts-crosextra-carlito",
        "node": "sudo apt install nodejs npm",
        "git": "sudo apt install git",
        "python": "sudo apt install python3 python3-venv",
    },
    "windows": {
        "poppler": "winget install -e --id oschwartz10612.Poppler  (then open a new terminal; "
                   "or unzip a release of github.com/oschwartz10612/poppler-windows and set "
                   "CVF_POPPLER_BIN to its Library\\bin folder)",
        "soffice": "winget install -e --id TheDocumentFoundation.LibreOffice",
        "node": "winget install -e --id OpenJS.NodeJS.LTS",
        "git": "winget install -e --id Git.Git",
        "python": "winget install -e --id Python.Python.3.13",
    },
}


def system():
    return "windows" if WINDOWS else "mac" if MAC else "linux"


def hint(program):
    """Install hint for a program on this system."""
    key = ("poppler" if program in POPPLER else "node" if program in ("node", "npm", "npx")
           else "python" if program.startswith("python") else program)
    return HINTS[system()].get(key, "")


class MissingProgram(FileNotFoundError):
    pass


def _env_paths(*names):
    return [Path(v) for v in (os.environ.get(n) for n in names) if v]


def _known_folders(program):
    """Usual install folders, used when the program is not in PATH."""
    if WINDOWS:
        programs = _env_paths("ProgramFiles", "ProgramFiles(x86)", "ProgramW6432") + [
            Path(r"C:\Program Files"), Path(r"C:\Program Files (x86)")]
        local = _env_paths("LOCALAPPDATA")
        home = Path.home()
        if program == "soffice":
            return [p / "LibreOffice" / "program" for p in programs]
        if program in POPPLER:
            winget = [b / "Microsoft" / "WinGet" / "Packages" for b in local] + [
                p / "WinGet" / "Packages" for p in programs]
            folders = [Path(f) for base in winget for f in sorted(glob.glob(
                str(base / "*oppler*" / "*" / "Library" / "bin")))]
            folders += [Path(f) for base in programs + [Path("C:\\")] for f in sorted(glob.glob(
                str(base / "poppler*" / "Library" / "bin")))]
            folders += [base / "Microsoft" / "WinGet" / "Links" for base in local]
            folders += [p / "chocolatey" / "bin" for p in _env_paths("ProgramData")]
            folders += [home / "scoop" / "shims"]
            folders += [home / d / "Library" / "bin" for d in ("miniconda3", "anaconda3", "miniforge3")]
            return folders
        if program in ("node", "npm", "npx"):
            return [p / "nodejs" for p in programs] + [Path(a) / "npm" for a in _env_paths("APPDATA")]
        if program == "git":
            return [p / "Git" / "cmd" for p in programs]
        return []
    folders = [Path("/opt/homebrew/bin"), Path("/usr/local/bin"), Path("/usr/bin")]
    if MAC and program == "soffice":
        folders.insert(0, Path("/Applications/LibreOffice.app/Contents/MacOS"))
    return folders


def _executable_names(program):
    if not WINDOWS:
        return [program]
    if program in ("npm", "npx"):
        return [program + ".cmd", program + ".exe"]
    return [program + ".exe", program + ".com", program + ".cmd"]


def find(program):
    """Full path of a program, or None."""
    names = _executable_names(program)
    if program in POPPLER:
        for folder in _env_paths(POPPLER_ENV):
            for name in names:
                if (folder / name).is_file():
                    return str(folder / name)
    if WINDOWS and program == "soffice":
        # soffice.com is the console launcher: it waits for the conversion and keeps the output.
        for folder in _known_folders(program):
            if (folder / "soffice.com").is_file():
                return str(folder / "soffice.com")
    found = shutil.which(program)
    if found:
        return found
    for folder in _known_folders(program):
        for name in names:
            if (folder / name).is_file():
                return str(folder / name)
    return None


def require(program):
    found = find(program)
    if found is None:
        extra = f" (or set {POPPLER_ENV} to the folder that has it)" if program in POPPLER else ""
        raise MissingProgram(f'"{program}" was not found{extra}; install it: {hint(program)}')
    return found


def venv_python():
    return VENV / ("Scripts/python.exe" if WINDOWS else "bin/python")


def node_package(name, prefix=LOCAL_NODE):
    """Folder of a package installed with npm install -g --prefix <prefix>, or None."""
    for folder in (prefix / "lib" / "node_modules" / name, prefix / "node_modules" / name):
        if folder.is_dir():
            return folder
    return None


def cache_dir():
    xdg = os.environ.get("XDG_CACHE_HOME")
    if xdg:
        return Path(xdg)
    if WINDOWS and os.environ.get("LOCALAPPDATA"):
        return Path(os.environ["LOCALAPPDATA"])
    return Path.home() / ".cache"


def utf8_console():
    """Print UTF-8 (✅, ❌, accents) on any console or pipe instead of failing on Windows."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass
