"""FastAPI entrypoint that safely coexists with the existing Django app.

FastAPI handles a small set of service endpoints under `/fastapi/*`,
while every existing Django route remains available under `/`.
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.core.asgi import get_asgi_application
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lydo_project.settings")

# Keep Django's ASGI app behind FastAPI so we can add service endpoints
# without rewriting the existing site routing.
django_app = ASGIStaticFilesHandler(get_asgi_application())
trusted_hosts = list(settings.ALLOWED_HOSTS or [])

if settings.DEBUG and not trusted_hosts:
    trusted_hosts = ["127.0.0.1", "localhost"]

app = FastAPI(
    title="LYDO FastAPI Gateway",
    description="FastAPI service mounted alongside the existing Django application.",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG or os.environ.get("FASTAPI_ENABLE_DOCS") == "1" else None,
    redoc_url="/redoc" if settings.DEBUG or os.environ.get("FASTAPI_ENABLE_DOCS") == "1" else None,
    openapi_url="/openapi.json" if settings.DEBUG or os.environ.get("FASTAPI_ENABLE_DOCS") == "1" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=(["*"] if getattr(settings, "CORS_ALLOW_ALL_ORIGINS", False) else list(getattr(settings, "CORS_ALLOWED_ORIGINS", []))),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if trusted_hosts and "*" not in trusted_hosts:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts)


@app.get("/fastapi/health", tags=["FastAPI"])
async def fastapi_health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "fastapi",
        "django": "mounted",
    }


@app.get("/fastapi/info", tags=["FastAPI"])
async def fastapi_info() -> dict[str, object]:
    return {
        "message": "FastAPI is active and serving alongside Django.",
        "fastapi_docs": app.docs_url,
        "fastapi_health": "/fastapi/health",
        "static_url": settings.STATIC_URL,
        "django_admin": "/admin/",
        "django_root": "/",
        "debug": settings.DEBUG,
        "allowed_hosts": trusted_hosts,
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> RedirectResponse:
    """Serve the browser favicon request from the existing shared logo asset."""
    return RedirectResponse(url=f"{settings.STATIC_URL}images/logo.png", status_code=307)


@app.on_event("startup")
async def start_background_services() -> None:
    """Start background jobs once when the FastAPI process boots."""
    from monitoring.age_rules import start_aged_out_cleanup_scheduler

    start_aged_out_cleanup_scheduler()

# Mount Django last so explicit FastAPI routes above take priority.
app.mount("/", django_app)
