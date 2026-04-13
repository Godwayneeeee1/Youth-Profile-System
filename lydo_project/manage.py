#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks via Django's management command runner."""
    # Point Django at the project settings module before any imports.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lydo_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Delegate to Django's CLI with the arguments passed to this script.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
