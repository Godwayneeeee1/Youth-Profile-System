"""Age eligibility helpers and a background cleanup scheduler."""
import datetime
import logging
import os
import sys
import threading
from pathlib import Path

from django.conf import settings
from django.db import close_old_connections

logger = logging.getLogger(__name__)

_SCHEDULER_LOCK = threading.Lock()
_SCHEDULER_STARTED = False
_SCHEDULER_STOP_EVENT = threading.Event()
_SCHEDULER_PROCESS_LOCK_HANDLE = None
_SCHEDULER_SKIP_COMMANDS = {
    'makemigrations',
    'migrate',
    'collectstatic',
    'shell',
    'dbshell',
    'createsuperuser',
    'changepassword',
    'test',
}


def _is_runserver_parent_process():
    """Avoid starting background threads in Django's autoreload parent process."""
    return 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true'


def years_ago(reference_date, years):
    """Return the date that is N years before a reference date."""
    try:
        return reference_date.replace(year=reference_date.year - years)
    except ValueError:
        return reference_date.replace(month=2, day=28, year=reference_date.year - years)


def age_on_date(birthdate, reference_date=None):
    """Compute age as of a specific date (defaults to today)."""
    if not birthdate:
        return None
    reference_date = reference_date or datetime.date.today()
    return reference_date.year - birthdate.year - (
        (reference_date.month, reference_date.day) < (birthdate.month, birthdate.day)
    )


def is_birthdate_aged_out(birthdate, reference_date=None):
    """Return True if a birthdate exceeds the 30-years-old cutoff."""
    if not birthdate:
        return False
    reference_date = reference_date or datetime.date.today()
    return birthdate <= years_ago(reference_date, 31)


def oldest_allowed_birthdate(reference_date=None):
    """Return the earliest birthdate still allowed in the system."""
    reference_date = reference_date or datetime.date.today()
    return years_ago(reference_date, 31) + datetime.timedelta(days=1)


def purge_aged_out_youths(reference_date=None):
    """Delete aged-out youth records and return how many were removed."""
    from .models import Youth

    reference_date = reference_date or datetime.date.today()
    cutoff = years_ago(reference_date, 31)
    deleted_count, _ = Youth.objects.filter(
        birthdate__isnull=False,
        birthdate__lte=cutoff,
    ).delete()
    return deleted_count


def _should_skip_scheduler_start():
    """Guardrails to avoid starting the scheduler for management commands."""
    if os.environ.get('LYDO_DISABLE_AGE_OUT_SCHEDULER') == '1':
        return True
    if _is_runserver_parent_process():
        return True
    if any(command in sys.argv for command in _SCHEDULER_SKIP_COMMANDS):
        return True
    return False


def _cleanup_interval_seconds():
    """Read cleanup interval from settings with a 5-minute minimum."""
    return max(300, int(getattr(settings, 'AGE_OUT_CLEANUP_INTERVAL_SECONDS', 3600)))


def _scheduler_lock_path():
    """Lock file path used to prevent multiple schedulers per process group."""
    return Path(getattr(settings, 'BASE_DIR', Path.cwd())) / '.lydo_age_out_scheduler.lock'


def _acquire_scheduler_process_lock():
    """Ensure only one scheduler runs per process group (cross-platform lock)."""
    global _SCHEDULER_PROCESS_LOCK_HANDLE

    if _SCHEDULER_PROCESS_LOCK_HANDLE is not None:
        return True

    lock_file = open(_scheduler_lock_path(), 'a+b')

    try:
        if os.name == 'nt':
            import msvcrt

            lock_file.seek(0)
            lock_file.write(b'0')
            lock_file.flush()
            lock_file.seek(0)
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        lock_file.close()
        return False

    lock_file.seek(0)
    lock_file.truncate()
    lock_file.write(str(os.getpid()).encode('ascii', 'ignore') or b'0')
    lock_file.flush()
    _SCHEDULER_PROCESS_LOCK_HANDLE = lock_file
    return True


def _cleanup_loop():
    """Background loop that periodically removes aged-out records."""
    interval_seconds = _cleanup_interval_seconds()
    while not _SCHEDULER_STOP_EVENT.is_set():
        try:
            close_old_connections()
            deleted_count = purge_aged_out_youths()
            if deleted_count:
                logger.info("Age-out cleanup removed %s youth record(s).", deleted_count)
        except Exception:
            logger.exception("Age-out cleanup job failed.")
        finally:
            close_old_connections()

        if _SCHEDULER_STOP_EVENT.wait(interval_seconds):
            break


def start_aged_out_cleanup_scheduler():
    """Start the background cleanup thread if not already running."""
    global _SCHEDULER_STARTED

    if _should_skip_scheduler_start():
        return False

    with _SCHEDULER_LOCK:
        if _SCHEDULER_STARTED:
            return False
        if not _acquire_scheduler_process_lock():
            return False

        worker = threading.Thread(
            target=_cleanup_loop,
            name='lydo-age-out-cleanup',
            daemon=True,
        )
        worker.start()
        _SCHEDULER_STARTED = True
        return True
