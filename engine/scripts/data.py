# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Loads cv.json, applies the character policy and builds the view used by the templates.

The view is a list of blocks in the exact order they are read in the CV. It is used by
render_pdf.py, render_docx.py and the tests (to know which text must appear).
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STRINGS = json.loads((ROOT / "template" / "strings.json").read_text(encoding="utf-8"))

# Characters allowed besides printable ASCII (see research doc 05, §5.3 and §5.7).
EXTRA_ALLOWED = set("–—•‘’“”")
NORMALIZE = {" ": " ", "‐": "-", "‑": "-", "…": "...", "\t": " "}


def allowed_char(c):
    o = ord(c)
    if 0x20 <= o <= 0x7E or c in EXTRA_ALLOWED:
        return True
    if 0xA1 <= o <= 0xFF and o != 0xAD:  # Latin-1 without the soft hyphen
        return True
    return 0x100 <= o <= 0x17F  # Latin Extended-A


def clean(text, where, errors):
    """NFC + normalizations; records any forbidden character."""
    t = unicodedata.normalize("NFC", text)
    t = "".join(unicodedata.normalize("NFKC", c) if 0xFB00 <= ord(c) <= 0xFB06 else c for c in t)
    for a, b in NORMALIZE.items():
        t = t.replace(a, b)
    t = re.sub(r" {2,}", " ", t).strip()
    for c in t:
        if not allowed_char(c):
            errors.append(f"{where}: forbidden character U+{ord(c):04X} ({unicodedata.name(c, '?')})")
    return t


def clean_all(obj, where, errors):
    if isinstance(obj, str):
        return clean(obj, where, errors)
    if isinstance(obj, list):
        return [clean_all(v, f"{where}[{i}]", errors) for i, v in enumerate(obj)]
    if isinstance(obj, dict):
        return {k: clean_all(v, f"{where}.{k}", errors) for k, v in obj.items()}
    return obj


# In English, no accented letters or ñ, not even in proper names (the CV rules doc).
NO_DECOMPOSE = {"ß": "ss", "æ": "ae", "Æ": "AE", "ø": "o", "Ø": "O", "œ": "oe", "Œ": "OE",
                "đ": "d", "Đ": "D", "ð": "d", "Ð": "D", "ł": "l", "Ł": "L", "þ": "th",
                "Þ": "Th", "ı": "i", "ĸ": "k", "ŉ": "n", "¿": "", "¡": ""}


def allowed_in_english(c):
    return 0x20 <= ord(c) <= 0x7E or c in EXTRA_ALLOWED


def strip_accents(text, where, errors):
    """'San José' → 'San Jose', 'Tecnológico' → 'Tecnologico', 'Muñoz' → 'Munoz'."""
    t = "".join(NO_DECOMPOSE.get(c, c) for c in text)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = unicodedata.normalize("NFC", t)
    t = re.sub(r" {2,}", " ", t).strip()
    for c in t:
        if not allowed_in_english(c):
            errors.append(f"{where}: character not allowed in an English CV U+{ord(c):04X} "
                          f"({unicodedata.name(c, '?')})")
    return t


def strip_accents_all(obj, where, errors):
    if isinstance(obj, str):
        return strip_accents(obj, where, errors)
    if isinstance(obj, list):
        return [strip_accents_all(v, f"{where}[{i}]", errors) for i, v in enumerate(obj)]
    if isinstance(obj, dict):
        # Technical keys (sources, ids, dates) are left alone; only the texts change.
        return {k: (v if k in ("sources", "language", "paper") else strip_accents_all(v, f"{where}.{k}", errors))
                for k, v in obj.items()}
    return obj


def format_date(value, language, year_only=False):
    """'2025-10' → 'October 2025'; 'present' → 'Present'; 'in_progress' → 'In progress'.
    With year_only=True (education and certifications), '2018' → '2018' is also accepted."""
    tx = STRINGS[language]
    if value in (None, ""):
        return ""
    if value == "present":
        return tx["present"]
    if value == "in_progress":
        return tx["in_progress"]
    if year_only and re.fullmatch(r"\d{4}", value):
        return value
    m = re.fullmatch(r"(\d{4})-(\d{2})", value)
    if not m or not 1 <= int(m.group(2)) <= 12:
        allowed = "YYYY-MM, YYYY" if year_only else "YYYY-MM"
        raise ValueError(f"Invalid date '{value}': use {allowed}, 'present' or 'in_progress'")
    return f"{tx['months'][int(m.group(2)) - 1]} {m.group(1)}"


def date_range(start, end, language, year_only=False):
    a, b = format_date(start, language, year_only), format_date(end, language, year_only)
    return f"{a} – {b}" if a and b else (a or b)


def strict_dates(e, where):
    """Jobs and projects need month and year: a year alone is not enough for the tests and ATS."""
    for field in ("start", "end"):
        value = e.get(field)
        if isinstance(value, str) and re.fullmatch(r"\d{4}", value):
            raise ValueError(f"{where} \"{e.get('title') or e.get('name')}\": {field} '{value}' has only the "
                             "year; jobs need month and year; ask the person")


def entry_line(main, rest, dates):
    """Title (bold), rest | dates, all on one line (research doc 05, §5.2)."""
    rest_text = ", ".join(x for x in rest if x)
    return {"bold": main, "rest": (", " + rest_text) if rest_text else "",
            "dates": dates}


def load(path):
    """Returns (clean_cv, view, errors)."""
    raw = json.loads(Path(path).read_text(encoding="utf-8-sig"))  # -sig: also a file saved with a BOM
    errors = []
    cv = clean_all(raw, "cv", errors)
    language = cv.get("language", "en")
    if language not in STRINGS:
        errors.append(f"language '{language}' is not supported (en, es)")
        language = "en"
    if language == "en":
        cv = strip_accents_all(cv, "cv", errors)
    for field in ("name", "headline", "location", "email"):
        if not cv.get("contact", {}).get(field):
            errors.append(f"contact.{field} is required")
    try:
        view = build_view(cv, language)
    except (ValueError, KeyError) as e:
        errors.append(f"incomplete data: {e}")
        view = None
    return cv, view, errors


def build_view(cv, language):
    tx = STRINGS[language]
    c = cv["contact"]
    contact = [c[k] for k in ("location", "phone", "email", "linkedin", "portfolio") if c.get(k)]
    sections = []
    if cv.get("summary", {}).get("text"):
        sections.append({"id": "summary", "title": tx["summary"], "paragraph": cv["summary"]["text"]})
    if cv.get("skills"):
        lines = [{"label": s["category"] + ":", "text": ", ".join(s["items"])} for s in cv["skills"]]
        sections.append({"id": "skills", "title": tx["skills"], "labeled": lines})
    for key in ("experience", "projects"):
        entries = []
        for i, e in enumerate(cv.get(key, [])):
            strict_dates(e, f"{key}[{i}]")
            main = e.get("title") or e.get("name")
            rest = [e.get("company"), e.get("location")] if key == "experience" else [e.get("detail")]
            entries.append({**entry_line(main, rest, date_range(e.get("start"), e.get("end"), language)),
                            "bullets": [b["text"] for b in e.get("bullets", [])]})
        if entries:
            sections.append({"id": key, "title": tx[key], "entries": entries})
    if cv.get("education"):
        entries = [{**entry_line(e["degree"], [e.get("institution"), e.get("location")],
                                 date_range(e.get("start"), e.get("end"), language, year_only=True)),
                    "bullets": [b["text"] for b in e.get("bullets", [])]}
                   for e in cv["education"]]
        sections.append({"id": "education", "title": tx["education"], "entries": entries})
    if cv.get("certifications"):
        entries = [{**entry_line(e["name"], [e.get("issuer")],
                                 date_range(e.get("start"), e.get("expires"), language, year_only=True)),
                    "bullets": []}
                   for e in cv["certifications"]]
        sections.append({"id": "certifications", "title": tx["certifications"], "entries": entries})
    if cv.get("languages"):
        text = " | ".join(f"{i['language']} ({i['level']})" for i in cv["languages"])
        sections.append({"id": "languages", "title": tx["languages"], "paragraph": text})
    return {"language": language, "name": c["name"], "headline": c["headline"], "contact": contact,
            "sections": sections, "paper": cv.get("paper", "letter"),
            "pdf_title": f"{c['name']} – {tx['resume']}"}


def expected_text(view):
    """All visible text, in reading order, one logical line per element."""
    out = [view["name"], view["headline"], " | ".join(view["contact"])]
    for s in view["sections"]:
        out.append(s["title"])
        if "paragraph" in s:
            out.append(s["paragraph"])
        for l in s.get("labeled", []):
            out.append(f"{l['label']} {l['text']}")
        for e in s.get("entries", []):
            out.append(f"{e['bold']}{e['rest']}" + (f" | {e['dates']}" if e["dates"] else ""))
            out.extend(e["bullets"])
    return out


def file_name(view):
    base = unicodedata.normalize("NFKD", view["name"]).encode("ascii", "ignore").decode()
    return "-".join(base.split()) + "-" + STRINGS[view["language"]]["resume"]
