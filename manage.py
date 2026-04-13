#!/usr/bin/env python
"""Entry point for Django commands when the project root is the repo root.

This wrapper keeps Vercel's Django auto-detection happy while preserving the
existing project layout under ./lydo_project.
"""

import os
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    project_root = repo_root / "lydo_project"

    # Ensure the Django project package is importable.
    sys.path.insert(0, str(project_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lydo_project.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure dependencies are installed and "
            "your virtual environment is active."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
