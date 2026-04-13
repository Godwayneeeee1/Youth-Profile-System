"""Vercel entrypoint for the FastAPI application."""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.join(ROOT, "lydo_project")
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lydo_project.fastapi_app import app  # noqa: E402

__all__ = ["app"]
