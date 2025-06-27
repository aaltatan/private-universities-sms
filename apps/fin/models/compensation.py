from decimal import Decimal
from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_delete, pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals, validators
from apps.core.choices import RoundMethodChoices
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search, round_to_nearest

from ..constants import compensations as constants
from .tax import Tax


class CompensationManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("tax")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Compensation(AddCreateActivityMixin, AbstractUniqueNameModel):
    class CalculationUserChoices(models.TextChoices):
        FIXED = "fixed", _("fixed").title()
        BY_INPUT = "by_input", _("by input").title()

    class CalculationChoices(models.TextChoices):
        FIXED = "fixed", _("fixed").title()
        BY_INPUT = "by_input", _("by input").title()
        FORMULA = "formula", _("formula").title()

    class AffectedByWorkingDaysChoices(models.TextChoices):
        YES = True, _("yes").title()
        NO = False, _("no").title()

    class TaxClassificationChoices(models.TextChoices):
        SALARY = "salary", _("salary").title()
        WITHHOLDING_TAX_APPLICABLE = (
            "withholding_tax_applicable",
            _("withholding tax applicable").title(),
        )
        WITHHOLDING_TAX_NOT_APPLICABLE = (
            "withholding_tax_not_applicable",
            _("withholding tax not applicable").title(),
        )
        OTHERS = "others", _("others").title()

    shortname = models.CharField(
        max_length=255,
        verbose_name=_("short name"),
        blank=True,
        default="",
        help_text=_("to use it in services like sms, whatsapp, etc."),
    )
    calculation_method = models.CharField(
        verbose_name=_("calculation method"),
        max_length=10,
        choices=CalculationChoices.choices,
        default=CalculationChoices.BY_INPUT,
    )
    tax = models.ForeignKey(
        Tax,
        null=True,
        blank=True,
        verbose_name=_("tax"),
        on_delete=models.PROTECT,
        related_name="compensations",
    )
    tax_classification = models.CharField(
        verbose_name=_("tax classification"),
        max_length=255,
        choices=TaxClassificationChoices.choices,
        default=TaxClassificationChoices.WITHHOLDING_TAX_APPLICABLE,
        help_text=_(
            "classify the nature of compensation to know how to calculate it in the periodic tax statement"
        ),
    )
    round_method = models.CharField(
        verbose_name=_("round method"),
        max_length=10,
        choices=RoundMethodChoices.choices,
        default=RoundMethodChoices.CEIL,
    )
    rounded_to = models.PositiveIntegerField(
        verbose_name=_("rounded to"),
        default=1,
        validators=[MinValueValidator(1)],
    )
    value = models.DecimalField(
        verbose_name=_("value"),
        max_digits=20,
        decimal_places=4,
        default=0,
    )
    min_value = models.DecimalField(
        verbose_name=_("min value"),
        max_digits=20,
        decimal_places=4,
        default=0,
    )
    max_value = models.DecimalField(
        verbose_name=_("max value"),
        max_digits=20,
        decimal_places=4,
        default=500_000_000,
    )
    affected_by_working_days = models.BooleanField(
        verbose_name=_("affected by working days"),
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("is active"),
    )
    formula = models.TextField(
        verbose_name=_("formula"),
        blank=True,
        default="",
        help_text="""
        <strong>Formula to calculate compensation value</strong>
        <ul>
            <li>- It should be a valid python expression</li>
            <li>- It should return a decimal number</li>
            <li>- Always use `obj` as argument</li>
            <li>- You can use underscores (_) to separate numbers as thousands</li>
        </ul>
        """,
    )
    document = models.FileField(
        upload_to="compensations",
        verbose_name=_("document"),
        blank=True,
        null=True,
        validators=[
            validators.pdf_image_extension_validator,
            validators.validate_pdf_image_mimetype,
        ],
    )
    accounting_id = models.CharField(
        verbose_name=_("accounting id"),
        help_text=_("accounting id in accounting system (in chart of accounts)"),
        blank=True,
        null=True,
        max_length=15,
        default="31",
    )

    objects: CompensationManager = CompensationManager()

    def calculate(self, value: Decimal | int | float = 0, obj: Any = None) -> Decimal:
        """
        a method to calculate compensation value

        Args:
            value (Decimal | int | float): value to calculate
            obj (Any): an object to calculate value

        Returns:
            Decimal: calculated value
        """
        if not self.is_active:
            return Decimal(0)

        if self.calculation_method == self.CalculationChoices.BY_INPUT:
            result = value
        elif self.calculation_method == self.CalculationChoices.FIXED:
            result = self.value
        elif self.calculation_method == self.CalculationChoices.FORMULA:
            try:
                # formula should like this
                # `2000 if obj.gender == "male" else 1000`
                result = eval(self.formula)
            except:  # noqa: E722
                result = 0

        return round_to_nearest(result, self.round_method, self.rounded_to)

    def clean(self):
        errors: dict[str, ValidationError] = {}

        if self.calculation_method == self.CalculationChoices.FIXED:
            if self.value == 0:
                errors["value"] = ValidationError(
                    _("value must be greater than 0."),
                )

            if self.min_value > self.value:
                errors["value"] = ValidationError(
                    _("min value must be less than value."),
                )

            if self.max_value < self.value:
                errors["value"] = ValidationError(
                    _("max value must be greater than value."),
                )

        if self.min_value >= self.max_value:
            errors["min_value"] = ValidationError(
                _("min value must be less than max value."),
            )

        if self.calculation_method == self.CalculationChoices.FORMULA:
            if self.formula == "":
                errors["formula"] = ValidationError(
                    _("formula must be filled."),
                )

        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        result = self.name

        if self.calculation_method == self.CalculationChoices.FIXED:
            result += f" ({self.value:,.2f})"

        if self.is_active is False:
            result += _(" (not activated)")

        return result

    class Meta:
        icon = "banknotes"
        ordering = ("-is_active", "tax__name", "calculation_method", "name")
        codename_plural = "compensations"
        verbose_name = _("compensation").title()
        verbose_name_plural = _("compensations").title()
        permissions = (
            ("export_compensation", "Can export compensation"),
            ("view_activity_compensation", "Can view compensation activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    def get_tax(self, obj: Compensation) -> str:
        return obj.tax.name if obj.tax else "-"

    class Meta:
        model = Compensation
        fields = (
            "name",
            "shortname",
            "calculation_method",
            "tax",
            "tax_classification",
            "round_method",
            "rounded_to",
            "value",
            "affected_by_working_days",
            "is_active",
            "formula",
            "description",
        )


def clean_value(sender: Any, instance: Compensation, *args, **kwargs) -> None:
    if (
        instance.calculation_method == instance.CalculationChoices.BY_INPUT
        or instance.calculation_method == instance.CalculationChoices.FORMULA
    ):
        instance.value = 0


def compensation_post_delete(sender, instance: Compensation, *args, **kwargs):
    instance.document.delete()


pre_save.connect(signals.slugify_name, sender=Compensation)
pre_save.connect(clean_value, sender=Compensation)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Compensation)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Compensation)
post_delete.connect(compensation_post_delete, sender=Compensation)
