from decimal import Decimal

from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core import signals
from apps.core.choices import RoundMethodChoices
from apps.core.exceptions import FormulaNotValid
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search, round_to_nearest

from ..constants import taxes as constants


class TaxQuerySet(models.QuerySet):
    def annotate_compensations_count(self):
        return self.annotate(
            compensations_count=models.Count("compensations", distinct=True),
        )

    def annotate_brackets_count(self):
        return self.annotate(
            brackets_count=models.Count("brackets", distinct=True),
        )


class TaxManager(models.Manager):
    def annotate_compensations_count(self):
        return self.get_queryset().annotate_compensations_count()

    def annotate_brackets_count(self):
        return self.get_queryset().annotate_brackets_count()

    def get_queryset(self):
        queryset = TaxQuerySet(self.model, using=self._db)
        return queryset.prefetch_related("brackets", "compensations").annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )


class Tax(AddCreateActivityMixin, AbstractUniqueNameModel):
    class AffectedByWorkingDaysChoices(models.TextChoices):
        YES = True, _("yes")
        NO = False, _("no")

    class CalculationMethodChoices(models.TextChoices):
        FIXED_AMOUNT = "fixed_amount", _("fixed amount")
        FIXED_PERCENTAGE = "fixed_percentage", _("fixed percentage")
        BRACKETS = "brackets", _("brackets")
        FORMULA = "formula", _("formula")

    shortname = models.CharField(
        max_length=255,
        verbose_name=_("short name"),
        help_text=_("to use it in services like sms, whatsapp, etc."),
    )
    calculation_method = models.CharField(
        verbose_name=_("calculation method"),
        max_length=30,
        choices=CalculationMethodChoices.choices,
        default=CalculationMethodChoices.FIXED_AMOUNT,
    )
    amount = models.DecimalField(
        verbose_name=_("amount"),
        max_digits=20,
        decimal_places=4,
        default=0,
        help_text=_("if you choose fixed amount, this field will be used"),
    )
    percentage = models.DecimalField(
        verbose_name=_("percentage"),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_("if you choose fixed percentage, this field will be used"),
    )
    formula = models.TextField(
        verbose_name=_("formula"),
        blank=True,
        default="",
        help_text="""
        <strong>Formula to calculate tax value</strong>
        <ul>
            <li>- It should be a valid python expression</li>
            <li>- It should return a decimal number</li>
            <li>- You can use (compensation, employee and quantity) objects to calculate the value if based on any one of them</li>
            <li>- You can use underscores (_) to separate numbers as thousands</li>
        </ul>
        """,
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
    accounting_id = models.CharField(
        verbose_name=_("accounting id"),
        help_text=_("accounting id in accounting system (in chart of accounts)"),
        blank=True,
        null=True,
        max_length=15,
        default="31",
    )
    journals = GenericRelation(
        "trans.JournalEntry",
        related_query_name="tax",
        related_name="tax",
        object_id_field="fiscal_object_id",
        content_type_field="content_type",
    )

    objects: TaxManager = TaxManager()

    def clean(self):
        errors: dict[str, str] = {}

        if (
            self.pk
            and self.brackets.all().exists()
            and self.calculation_method != self.CalculationMethodChoices.BRACKETS
        ):
            errors["calculation_method"] = _(
                "you can't have brackets if the calculation method is not brackets."
            )

        if (
            self.calculation_method == self.CalculationMethodChoices.FORMULA
            and self.formula == ""
        ):
            errors["formula"] = _("formula must be filled.")

        if (
            self.calculation_method == self.CalculationMethodChoices.FIXED_AMOUNT
            and self.amount == 0
        ):
            errors["amount"] = _("amount must be greater than 0.")

        if (
            self.calculation_method == self.CalculationMethodChoices.FIXED_PERCENTAGE
            and self.percentage == 0
        ):
            errors["percentage"] = _("percentage must be greater than 0.")

        if errors:
            raise ValidationError(errors)

    def _calculate_fixed_amount(
        self, amount: Decimal | int | float, **context
    ) -> Decimal:
        return self.amount

    def _calculate_fixed_percentage(
        self, amount: Decimal | int | float, **context
    ) -> Decimal:
        return amount * self.percentage

    def _calculate_formula(self, amount: Decimal | int | float, **context) -> Decimal:
        try:
            # formula should like this
            # `2000 if obj.gender == "male" else 1000`
            return eval(self.formula)
        except Exception as e:
            raise FormulaNotValid(*e.args)

    def _calculate_brackets(self, amount: Decimal | int | float, **context) -> Decimal:
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
        self, amount: Decimal | int | float, rounded: bool = False, **context
    ) -> Decimal:
        methods_map = {
            self.CalculationMethodChoices.FIXED_AMOUNT: self._calculate_fixed_amount,
            self.CalculationMethodChoices.FIXED_PERCENTAGE: self._calculate_fixed_percentage,
            self.CalculationMethodChoices.BRACKETS: self._calculate_brackets,
            self.CalculationMethodChoices.FORMULA: self._calculate_formula,
        }

        tax = methods_map[self.calculation_method](amount=amount, **context)

        if rounded:
            return round_to_nearest(
                number=tax, to_nearest=self.rounded_to, method=self.round_method
            )
        else:
            return tax

    class Meta:
        icon = "receipt-percent"
        ordering = ("calculation_method", "name")
        codename_plural = "taxes"
        verbose_name = _("tax")
        verbose_name_plural = _("taxes")
        permissions = (
            ("export_tax", "Can export tax"),
            ("view_activity_tax", "Can view tax activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = (
            "name",
            "shortname",
            "calculation_method",
            "amount",
            "percentage",
            "formula",
            "round_method",
            "rounded_to",
            "accounting_id",
            "description",
        )


def pre_save_tax(sender, instance: Tax, *args, **kwargs):
    if instance.calculation_method == instance.CalculationMethodChoices.FORMULA:
        instance.amount = 0
        instance.percentage = 0

    if instance.calculation_method == instance.CalculationMethodChoices.FIXED_AMOUNT:
        instance.percentage = 0
        instance.formula = ""

    if (
        instance.calculation_method
        == instance.CalculationMethodChoices.FIXED_PERCENTAGE
    ):
        instance.amount = 0
        instance.formula = ""


pre_save.connect(signals.slugify_name, sender=Tax)
pre_save.connect(pre_save_tax, sender=Tax)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Tax)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Tax)
