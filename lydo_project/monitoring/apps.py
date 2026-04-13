"""App configuration for the monitoring module."""
from django.apps import AppConfig


class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'

    def ready(self):
        # Start the age-out cleanup scheduler when the app is loaded.
        from .age_rules import start_aged_out_cleanup_scheduler

        start_aged_out_cleanup_scheduler()
