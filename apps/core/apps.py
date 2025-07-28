from django.apps import AppConfig
from django.core.cache import cache


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        from .models import GlobalSetting

        cache.set("global_settings", GlobalSetting.get_settings(), None)
