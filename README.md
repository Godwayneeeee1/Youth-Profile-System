# LYDO Monitoring System

A Django-based web application designed for the Local Youth Development Office (LYDO) to monitor and manage youth records across different barangays.

## FastAPI / Uvicorn Deployment

The project can also run through the shared FastAPI gateway, which mounts the full Django app under `/` and exposes FastAPI service endpoints under `/fastapi/*`.

### Local run

```bash
python run_api.py
```

### Production-style environment variables

```bash
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=change-this-in-production
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,your-domain.com
DJANGO_CORS_ALLOWED_ORIGINS=https://your-domain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.com
DJANGO_SESSION_COOKIE_SECURE=1
DJANGO_CSRF_COOKIE_SECURE=1
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8001
UVICORN_RELOAD=0
```

### Production notes

- The FastAPI gateway serves Django static assets, including admin assets.
- FastAPI docs are enabled by default in debug mode. Set `FASTAPI_ENABLE_DOCS=1` if you want docs exposed while `DJANGO_DEBUG=0`.
- The age-out cleanup scheduler starts once per process group with a lock file so it behaves correctly under Uvicorn reload/workers.
- For public deployment behind Nginx, Caddy, or another reverse proxy, make sure your proxy forwards `X-Forwarded-Proto`.

## 📋 Prerequisites
Before setting this up on a new PC, ensure you have the following installed:
* **Python 3.10 or higher**: [Download here](https://www.python.org/downloads/) (Make sure to check "Add Python to PATH" during installation).
* **Git**: [Download here](https://git-scm.com/downloads).

---

## 🚀 Setup Instructions

Follow these steps to get the project running on a new machine:

### 1. Clone the Repository
Open your terminal (Command Prompt, PowerShell, or Git Bash) and run:
```bash
git clone [https://github.com/IceKrispy/Lydo_Monitoring_System.git](https://github.com/IceKrispy/Lydo_Monitoring_System.git)
cd Lydo_Monitoring_System
