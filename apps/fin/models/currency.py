from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import currencies as constants


class CurrencyManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Currency(AddCreateActivityMixin, AbstractUniqueNameModel):
    class IsPrimaryChoices(models.IntegerChoices):
        YES = True, _("primary").title()
        NO = False, _("secondary").title()

    symbol = models.CharField(
        max_length=10,
        verbose_name=_("symbol"),
    )
    code = models.CharField(
        max_length=3,
        unique=True,
        help_text=_("ISO 4217 3-letter currency code"),
    )
    fraction_name = models.CharField(
        max_length=20,
        verbose_name=_("fraction name"),
    )
    decimal_places = models.PositiveSmallIntegerField(
        default=2,
        help_text=_(
            "standard number of decimal places for this currency",
        ),
    )
    is_primary = models.BooleanField(
        verbose_name=_("is primary"),
        default=False,
        help_text=_("is it primary or secondary currency?"),
    )

    objects: CurrencyManager = CurrencyManager()

    class Meta:
        icon = "currency-dollar"
        codename_plural = "currencies"
        verbose_name = _("currency").title()
        verbose_name_plural = _("currencies").title()
        ordering = ("-is_primary", "name")
        permissions = (
            ("export_currency", "Can export currency"),
            ("view_activity_currency", "Can view currency activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            "name",
            "symbol",
            "code",
            "fraction_name",
            "decimal_places",
            "is_primary",
            "description",
        )


pre_save.connect(signals.slugify_name, sender=Currency)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Currency)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Currency)
