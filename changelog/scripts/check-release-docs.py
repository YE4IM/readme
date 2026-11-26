#!/usr/bin/env python3
"""Changelog entry point for the shared release-document checker."""

import runpy
from pathlib import Path

TARGET = Path(__file__).resolve().parents[2] / "releases" / "scripts" / "check-release-docs.py"
_loaded = runpy.run_path(str(TARGET))
globals().update({key: value for key, value in _loaded.items() if not key.startswith("__")})

if __name__ == "__main__":
    raise SystemExit(main())
