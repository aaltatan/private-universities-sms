from typing import Any
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models.abstracts import UrlsMixin
from apps.core.utils import annotate_search

from ..constants import tax_brackets as constants
from .tax import Tax


class TaxBracketManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("tax")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class TaxBracket(AddCreateActivityMixin, UrlsMixin, models.Model):
    tax = models.ForeignKey(
        Tax,
        verbose_name=_("tax"),
        on_delete=models.PROTECT,
        related_name="brackets",
    )
    amount_from = models.DecimalField(
        verbose_name=_("amount from"),
        max_digits=20,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    amount_to = models.DecimalField(
        verbose_name=_("amount to"),
        max_digits=20,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    rate = models.DecimalField(
        verbose_name=_("rate"),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    notes = models.TextField(
        verbose_name=_("notes"),
        blank=True,
        default="",
    )
    ordering = models.PositiveIntegerField(default=0)  # to order objects in inlines
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        default=None,
        allow_unicode=True,
    )

    objects: TaxBracketManager = TaxBracketManager()

    def clean(self):
        errors: dict[str, ValidationError] = {}

        if (
            getattr(self, "tax", None)
            and self.tax.calculation_method != Tax.CalculationMethodChoices.BRACKETS
        ):
            errors["tax"] = ValidationError(
                _("you can't add a bracket to a not brackets tax."),
            )
            errors["amount_from"] = ValidationError(
                _("you can't add a bracket to a not brackets tax."),
            )

        if self.amount_from == self.amount_to:
            errors["amount_from"] = ValidationError(
                _("amount from must be greater than amount to."),
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        return f"{self.tax.name} - {self.amount_from} - {self.amount_to}"

    class Meta:
        icon = "receipt-percent"
        ordering = ("tax", "amount_from", "amount_to")
        codename_plural = "tax_brackets"
        verbose_name = _("tax bracket")
        verbose_name_plural = _("tax brackets")
        permissions = (
            ("export_taxbracket", "Can export tax bracket"),
            ("view_activity_taxbracket", "Can view tax bracket activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    tax = serializers.CharField(source="tax.name")

    class Meta:
        model = TaxBracket
        fields = ("tax", "amount_from", "amount_to", "rate", "notes")


def slugify_bracket(
    sender: Any,
    instance: TaxBracket,
    *args,
    **kwargs: dict[str, Any],
) -> None:
    if instance.pk is None:
        instance.slug = uuid4().hex


pre_save.connect(slugify_bracket, sender=TaxBracket)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=TaxBracket)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=TaxBracket)
