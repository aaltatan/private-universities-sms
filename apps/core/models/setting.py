from typing import Any

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext as _

from .abstracts import SingletonModelMixin


class GlobalSetting(SingletonModelMixin, models.Model):
    max_page_size = models.PositiveIntegerField(
        default=100,
        verbose_name=_("max page size"),
        help_text=_("max page size for pagination purposes"),
    )
    per_page = models.PositiveIntegerField(
        default=25,
        verbose_name=_("per page"),
        help_text=_("per page for pagination purposes"),
    )
    messages_timeout = models.PositiveIntegerField(
        default=7,
        verbose_name=_("messages timeout"),
        help_text=_("messages timeout in seconds"),
    )
    critical_confirmation_timeout = models.PositiveIntegerField(
        default=2,
        verbose_name=_("critical confirmation timeout"),
        help_text=_("critical confirmation timeout in seconds"),
    )
    per_page_list = models.JSONField(
        default=list[10, 25, 50, 100],
        verbose_name=_("per page list"),
        help_text=_("per page list for pagination purposes"),
    )

    @classmethod
    def get_settings(cls):
        return cls.objects.values(
            "max_page_size",
            "per_page",
            "messages_timeout",
            "critical_confirmation_timeout",
            "per_page_list",
        ).first()

    def __str__(self):
        return f"GlobalSetting(max_page_size={self.max_page_size}, per_page={self.per_page}, messages_timeout={self.messages_timeout}, critical_confirmation_timeout={self.critical_confirmation_timeout}, per_page_list={self.per_page_list})"

    class Meta:
        verbose_name = _("global setting").title()
        verbose_name_plural = _("global settings").title()
        ordering = ("id",)


def update_cache(
    sender: Any, instance: GlobalSetting, **kwargs: dict[str, Any]
) -> None:
    cache.set("global_settings", instance.get_settings(), None)


post_save.connect(update_cache, sender=GlobalSetting)
