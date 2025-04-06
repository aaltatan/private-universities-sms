import uuid
from typing import Any

from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models.abstracts import UrlsMixin
from apps.core.utils import annotate_search

from ..constants import exchange_rates as constants
from .currency import Currency


class ExchangeRateManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("currency")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class ExchangeRate(UrlsMixin, AddCreateActivityMixin, models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )
    currency = models.ForeignKey(
        Currency,
        related_name="rates",
        on_delete=models.PROTECT,
        verbose_name=_("currency"),
    )
    rate = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        verbose_name=_("rate"),
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name=_("date"),
    )
    notes = models.TextField(
        max_length=1000,
        default="",
        blank=True,
        verbose_name=_("notes"),
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        allow_unicode=True,
        null=True,
        blank=True,
    )

    objects: ExchangeRateManager = ExchangeRateManager()

    class Meta:
        icon = "document-currency-dollar"
        codename_plural = "exchange_rates"
        verbose_name = _("exchange rate").title()
        verbose_name_plural = _("exchange rates").title()
        ordering = ("-currency__is_primary", "created_at", "date")
        permissions = (
            ("export_exchangerate", "Can export exchange rate"),
            ("view_activity_exchangerate", "Can view exchange rate activity"),
        )

    def __str__(self) -> str:
        str_date = self.date.strftime("%Y-%m-%d")
        return f"{self.currency.name} / {str_date}"


class ActivitySerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source="currency.name")

    class Meta:
        model = ExchangeRate
        fields = ("currency", "date", "rate", "notes")


def slugify_exchange_rate(
    sender: Any, instance: ExchangeRate, *args, **kwargs: dict[str, Any]
) -> None:
    if instance.slug is None:
        instance.slug = uuid.uuid4().hex


pre_save.connect(slugify_exchange_rate, sender=ExchangeRate)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=ExchangeRate)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=ExchangeRate)
