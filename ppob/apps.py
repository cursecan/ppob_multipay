from django.apps import AppConfig


class PpobConfig(AppConfig):
    name = 'ppob'

    def ready(self):
        from . import signals
