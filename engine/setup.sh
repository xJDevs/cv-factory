#!/usr/bin/env bash
# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
# Kept so old instructions still work: runs setup.py (macOS, Linux and Windows) with the first Python 3.10+ it finds.
for p in python3 python py; do "$p" -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>/dev/null && exec "$p" "$(dirname "$0")/setup.py" "$@"; done; echo "NOT READY: Python 3.10 or newer was not found (see engine/README.md)"; exit 1
