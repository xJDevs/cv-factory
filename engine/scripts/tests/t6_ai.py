# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Test 6 — AI extraction: an agent WITHOUT context reads (a) the PDF and (b) only its plain
text, and fills the schema in t6_instructions.md. Here what it extracted is compared with the CV.

Files expected in the output folder (written by the agent, not by this test):
  ai-from-pdf.json  and  ai-from-text.json
"""
import json
import re

from common import Result
from t4_order import norm

FILES = (("ai-from-pdf.json", "AI from PDF"), ("ai-from-text.json", "AI from text"))


def expected(view, cv):
    c = cv["contact"]
    secs = {s["id"]: s for s in view["sections"]}
    entries = lambda sid: secs.get(sid, {}).get("entries", [])
    return {
        "name": c["name"], "email": c["email"], "phone": c.get("phone", ""),
        "experience": [{"title": e["title"], "company": e["company"], "dates": v["dates"]}
                       for e, v in zip(cv.get("experience", []), entries("experience"))],
        "education": [{"degree": e["degree"], "institution": e["institution"]} for e in cv.get("education", [])],
        "languages": [i["language"] for i in cv.get("languages", [])],
    }


def compare(label, extracted, want, r):
    for field in ("name", "email"):
        if norm(extracted.get(field, "")) != norm(want[field]):
            r.fail(f'{label}: {field} "{extracted.get(field)}" ≠ "{want[field]}"')
    if want["phone"] and re.sub(r"\D", "", want["phone"]) != re.sub(r"\D", "", extracted.get("phone", "")):
        r.fail(f'{label}: phone "{extracted.get("phone")}"')
    jobs = extracted.get("experience", [])
    if len(jobs) != len(want["experience"]):
        r.fail(f"{label}: {len(jobs)} jobs, there are {len(want['experience'])}")
    for w, s in zip(want["experience"], jobs):
        for field in ("title", "company", "dates"):
            if norm(s.get(field, "")) != norm(w[field]):
                r.fail(f'{label}: {field} "{s.get(field)}" ≠ "{w[field]}"')
    for w, s in zip(want["education"], extracted.get("education", [])):
        if norm(w["institution"]) not in norm(s.get("institution", "")):
            r.fail(f'{label}: institution "{s.get("institution")}" ≠ "{w["institution"]}"')
    languages = {norm(i.get("language", "")) for i in extracted.get("languages", [])}
    for i in want["languages"]:
        if norm(i) not in languages:
            r.fail(f'{label}: did not find the language "{i}"')


def run(ctx):
    r = Result(6, "AI extraction (agent without context, from PDF and from text)")
    want = expected(ctx["view"], ctx["cv"])
    for name, label in FILES:
        path = ctx["folder"] / name
        if not path.exists():
            r.fail(f"{label}: missing {name} (run the agent without context using t6_instructions.md)")
            continue
        compare(label, json.loads(path.read_text(encoding="utf-8-sig")), want, r)
    if r.passed:
        r.note("both agents extracted name, contact, jobs, education and languages without errors")
    return r
