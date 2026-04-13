"""Run the shared FastAPI + Django ASGI app with Uvicorn.

Usage:
    uvicorn --app-dir lydo_project lydo_project.fastapi_app:app --reload
    python run_api.py
"""

import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(ROOT, "lydo_project")
FRONTEND_ROOT = os.path.join(ROOT, "frontend")

# Ensure the Django project is importable when running as a script.
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def main() -> None:
    import uvicorn

    # Allow environment overrides for deployment while keeping local defaults.
    host = os.environ.get("UVICORN_HOST", "127.0.0.1")
    port = int(os.environ.get("UVICORN_PORT", "8001"))
    reload_enabled = os.environ.get("UVICORN_RELOAD", "1").strip().lower() in {"1", "true", "yes", "on"}
    log_level = os.environ.get("UVICORN_LOG_LEVEL", "info")

    # Run the FastAPI gateway (which mounts the Django app at "/").
    uvicorn.run(
        "lydo_project.fastapi_app:app",
        host=host,
        port=port,
        reload=reload_enabled,
        # Watch both backend and frontend assets so the dev server reloads on changes.
        reload_dirs=[PROJECT_ROOT, FRONTEND_ROOT],
        reload_includes=["*.py", "*.html", "*.css", "*.js"],
        log_level=log_level,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()
