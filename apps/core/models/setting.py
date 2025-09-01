from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


def default_per_page_list() -> list[int]:
    return [10, 25, 50, 100]


class GlobalSetting(SingletonModel):
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
        default=default_per_page_list,
        verbose_name=_("per page list"),
        help_text=_("per page list for pagination purposes"),
    )

    def __str__(self):
        return "Global Settings"

    class Meta:
        verbose_name = _("global settings")
        ordering = ("id",)
