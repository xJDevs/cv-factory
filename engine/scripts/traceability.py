# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Pre-check — Traceability: everything the CV says comes from a row of the source data, and
every achievement used is marked as verified. If something cannot be traced, nothing is generated.

The "snapshot" is built by reading the source databases live and COMPLETELY right before
generating the CV:
{"read_at": "YYYY-MM-DD HH:MM",
 "completeness": {"hub_read": true,
                  "databases": {"experience": {"rows_in_source": N}, "achievements": {...}, "skills": {...}}},
 "rows": {"<id>": {"database": "experience|achievements|skills", "url": "...", "text": "...",
                   "content": "<text of the page itself, may be empty>",
                   "verified": true|false|null}}}

Exhaustive reading: ALL rows of each database go in (also the unverified ones), each one
with its "content" (the page opened, not just the columns). "rows_in_source" is the total
the source shows for that database. If the numbers do not match, the CV is not generated.
"""
import json
from pathlib import Path

from common import Result

DATABASES = ("experience", "achievements", "skills")


def check_completeness(snap, r):
    comp = snap.get("completeness")
    if not comp:
        r.fail('the snapshot does not say whether the source was read completely (missing "completeness")')
        return
    if comp.get("hub_read") is not True:
        r.fail("the hub (Notion hub pages, or profile.json) was not read: read it and build the snapshot "
               "again with build_snapshot.py --hub-read")
    rows = snap.get("rows", {})
    for db in DATABASES:
        info = comp.get("databases", {}).get(db)
        if not info or not isinstance(info.get("rows_in_source"), int):
            r.fail(f'missing the total row count of the "{db}" database in the source')
            continue
        total = info["rows_in_source"]
        of_db = [f for f in rows.values() if f.get("database") == db]
        with_page = [f for f in of_db if isinstance(f.get("content"), str)]
        if total == 0:
            r.fail(f'the "{db}" database came back empty: check how the source was read')
        if len(of_db) != total:
            r.fail(f'"{db}": the source has {total} rows and the snapshot {len(of_db)}: the reading was not complete')
        if len(with_page) != len(of_db):
            r.fail(f'"{db}": {len(of_db) - len(with_page)} page(s) not opened and read')
    if r.passed:
        r.note("complete reading: " + ", ".join(
            f"{d} {comp['databases'][d]['rows_in_source']}" for d in DATABASES) + " rows, all opened and read")


def sources_of(cv):
    """(where, list of sources, requires_verified) for every claim in the CV."""
    yield "summary", cv.get("summary", {}).get("sources", []), True
    for i, s in enumerate(cv.get("skills", [])):
        yield f"skills[{i}] {s.get('category')}", s.get("sources", []), False
    for key in ("experience", "projects"):
        for i, e in enumerate(cv.get(key, [])):
            yield f"{key}[{i}] {e.get('title') or e.get('name')}", e.get("sources", []), False
            for j, b in enumerate(e.get("bullets", [])):
                yield f"{key}[{i}].bullets[{j}] \"{b.get('text', '')[:50]}\"", b.get("sources", []), True
    for key in ("education", "certifications", "languages"):
        for i, e in enumerate(cv.get(key, [])):
            yield f"{key}[{i}]", e.get("sources", []), False
            for j, b in enumerate(e.get("bullets", [])):
                yield f"{key}[{i}].bullets[{j}] \"{b.get('text', '')[:50]}\"", b.get("sources", []), True


def run(cv, snapshot_path):
    r = Result(0, "Traceability to the source data (confirmed facts only)")
    if not snapshot_path or not Path(snapshot_path).exists():
        r.fail("missing the snapshot of the source data read live (--snapshot)")
        return r
    snap = json.loads(Path(snapshot_path).read_text(encoding="utf-8-sig"))
    check_completeness(snap, r)
    rows = snap.get("rows", {})
    total = 0
    for where, ids, requires in sources_of(cv):
        if not ids:
            r.fail(f"{where}: does not say which source row it comes from")
            continue
        for rid in ids:
            total += 1
            row = rows.get(rid)
            if row is None:
                r.fail(f"{where}: row {rid} is not in the snapshot")
            elif row.get("database") == "achievements" and row.get("verified") is not True:
                r.fail(f"{where}: row {rid} is not marked as verified")
            elif requires and row.get("database") not in ("achievements", "experience"):
                r.fail(f'{where}: a claim must come from an achievement or an experience row, not from "{row.get("database")}"')
    if r.passed:
        r.note(f"{total} references to the source data checked (read at {snap.get('read_at', '?')})")
    return r
