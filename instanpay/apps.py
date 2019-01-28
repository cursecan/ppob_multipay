from django.apps import AppConfig


class InstanpayConfig(AppConfig):
    name = 'instanpay'

    def ready(self):
        from . import signals