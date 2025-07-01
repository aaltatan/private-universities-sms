from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.choices import RoundMethodChoices
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search, round_to_nearest

from ..constants import taxes as constants


class TaxManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("brackets", "compensations")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
                brackets_count=models.Count("brackets"),
                compensations_count=models.Count("compensations"),
            )
        )


class Tax(AddCreateActivityMixin, AbstractUniqueNameModel):
    class FixedChoices(models.TextChoices):
        FIXED = True, _("fixed").title()
        BRACKETS = False, _("brackets").title()

    class AffectedByWorkingDaysChoices(models.TextChoices):
        YES = True, _("yes").title()
        NO = False, _("no").title()

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
    affected_by_working_days = models.BooleanField(
        verbose_name=_("affected by working days"),
        default=False,
    )

    objects: TaxManager = TaxManager()

    def _calculate_fixed(self, amount: Decimal | int | float) -> Decimal:
        return amount * self.rate

    def _calculate_brackets(self, amount: Decimal | int | float) -> Decimal:
        brackets = self.brackets.all().order_by("amount_from")
        tax = 0
        for bracket in brackets:
            if bracket.amount_from <= amount <= bracket.amount_to:
                bracket_tax = bracket.rate * (amount - bracket.amount_from)
                tax += bracket_tax
                return tax
            else:
                tax += (bracket.amount_to - bracket.amount_from) * bracket.rate

        return tax

    def calculate(
        self, amount: Decimal | int | float, rounded: bool = False
    ) -> Decimal:
        if self.fixed:
            tax = self._calculate_fixed(amount=amount)
        else:
            tax = self._calculate_brackets(amount=amount)

        if rounded:
            return round_to_nearest(
                number=tax, to_nearest=self.rounded_to, method=self.round_method
            )
        else:
            return tax

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
