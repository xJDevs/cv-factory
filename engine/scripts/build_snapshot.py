# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Builds snapshot.json (the picture of the source data the engine uses) from a complete reading.

Input: a folder with experience.json, achievements.json and skills.json, each one with
{"database", "rows_in_source", "rows": [{"url", "properties", "content"}]}: every row of the
database, and every page opened and read (see README, "How a CV is made", step 1).
A row may have an explicit "id" instead of a "url" (for spreadsheet sources).

The schema file says which properties make up each row's "text", and which property (if any)
marks an achievement as verified:
{"experience":   {"text_fields": ["Name", "English title", ...], "verified_field": null},
 "achievements": {"text_fields": ["Description", ...], "verified_field": "Verified"},
 "skills":       {"text_fields": ["Skill", "Level", "Notes"], "verified_field": null}}
A row is verified when properties[verified_field] == "__YES__".

Usage: python3 build_snapshot.py <read-folder> <out/snapshot.json> --schema <schema.json> --hub-read

--hub-read says that the hub was read in this same reading: the hub page and its other pages
(such as search preferences) for Notion, or profile.json for a spreadsheet source. Without it,
"hub_read" is false and the traceability pre-check fails, so pass it only when that is true.

IDs are the database letter + the last 6 characters of the page id in the url
(E = experience, A = achievements, S = skills). They are stable between readings.
A row with an explicit "id" and no "url" keeps that id as-is.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import platform_tools

PREFIX = {"experience": "E", "achievements": "A", "skills": "S"}


def as_text(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(as_text(v) for v in value if as_text(v))
    return str(value).strip()


def row_text(fields, props):
    return " | ".join(t for t in (as_text(props.get(f)) for f in fields) if t)


def row_id(db, letter, row):
    url = row.get("url")
    if url:
        return letter + url.rstrip("/").split("/")[-1].split("?")[0][-6:]
    if row.get("id"):
        return str(row["id"])
    sys.exit(f'"{db}": a row has neither "url" nor "id"')


def main(folder, out, schema_path, hub_read):
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8-sig"))
    rows, comp = {}, {"hub_read": hub_read, "databases": {}}
    for db, letter in PREFIX.items():
        if db not in schema:
            sys.exit(f'the schema has no entry for "{db}"')
        fields = schema[db].get("text_fields", [])
        verified_field = schema[db].get("verified_field")
        d = json.loads((Path(folder) / f"{db}.json").read_text(encoding="utf-8-sig"))
        comp["databases"][db] = {"rows_in_source": d["rows_in_source"]}
        for row in d["rows"]:
            rid = row_id(db, letter, row)
            if rid in rows:
                sys.exit(f"duplicate id: {rid}")
            props = row.get("properties", {})
            verified = (props.get(verified_field) == "__YES__") if verified_field else None
            rows[rid] = {"database": db, "url": row.get("url"), "text": row_text(fields, props),
                         "content": row.get("content", ""), "verified": verified}
    snap = {"read_at": datetime.now().strftime("%Y-%m-%d %H:%M"), "completeness": comp, "rows": rows}
    Path(out).write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print({d: v["rows_in_source"] for d, v in comp["databases"].items()}, "→", len(rows), "rows")
    if not hub_read:
        print("WARNING: --hub-read was not given, so hub_read is false and the CV pre-check will fail. "
              "Read the hub (Notion hub pages, or profile.json) and build the snapshot again with --hub-read.")


if __name__ == "__main__":
    platform_tools.utf8_console()
    ap = argparse.ArgumentParser(description="Build snapshot.json from a complete reading of the source databases.")
    ap.add_argument("folder", help="folder with experience.json, achievements.json and skills.json")
    ap.add_argument("out", help="path of the snapshot.json to write")
    ap.add_argument("--schema", required=True, help="schema.json: text fields and verified field per database")
    ap.add_argument("--hub-read", action="store_true",
                    help="the hub (Notion hub pages, or profile.json) was read in this same reading; "
                         "without it the traceability pre-check fails")
    a = ap.parse_args()
    main(a.folder, a.out, a.schema, a.hub_read)
