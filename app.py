"""Deployment entrypoint for the FastAPI application.

This file exists so platforms that auto-detect FastAPI can find `app`
at the repository root.
"""

from __future__ import annotations

import os
import sys

# Ensure the inner Django/FastAPI package is importable when the repo root
# is on the PYTHONPATH (common for platform auto-detection).
ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(ROOT, "lydo_project")
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lydo_project.fastapi_app import app  # noqa: E402

__all__ = ["app"]
