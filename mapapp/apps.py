from django.apps import AppConfig


class MapappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mapapp'

    def ready(self):
        # Event handler'ları yükle
        from . import events
