from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search, round_to_nearest

from ..constants import taxes as constants


class TaxManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("brackets")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Tax(AddCreateActivityMixin, AbstractUniqueNameModel):
    class FixedChoices(models.TextChoices):
        FIXED = True, _("fixed").title()
        BRACKETS = False, _("brackets").title()

    class RoundMethodChoices(models.TextChoices):
        ROUND = "round", _("normal").title()
        FLOOR = "floor", _("down").title()
        CEIL = "ceil", _("up").title()

    objects: TaxManager = TaxManager()

    fixed = models.BooleanField(
        default=True,
        verbose_name=_("fixed"),
    )
    rate = models.DecimalField(
        verbose_name=_("rate"),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    rounded_to = models.PositiveIntegerField(
        verbose_name=_("rounded to"),
        default=1,
        validators=[MinValueValidator(1)],
    )
    round_method = models.CharField(
        verbose_name=_("round method"),
        max_length=10,
        choices=RoundMethodChoices.choices,
        default=RoundMethodChoices.CEIL,
    )

    def calculate(self, amount: Decimal | int | float) -> Decimal:
        if self.fixed:
            tax = amount * self.rate
            return round_to_nearest(
                number=tax,
                method=self.round_method,
                to_nearest=self.rounded_to,
            )

        return Decimal(0)

    class Meta:
        icon = "receipt-percent"
        ordering = ("fixed", "name")
        codename_plural = "taxes"
        verbose_name = _("tax").title()
        verbose_name_plural = _("taxes").title()
        permissions = (
            ("export_tax", "Can export tax"),
            ("view_activity_tax", "Can view tax activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ("name", "fixed", "rate", "rounded_to", "description")


pre_save.connect(signals.slugify_name, sender=Tax)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Tax)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Tax)
