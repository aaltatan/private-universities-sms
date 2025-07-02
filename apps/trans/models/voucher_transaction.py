import uuid
from decimal import Decimal
from typing import Literal

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.exceptions import FormulaNotValid
from apps.core.models import TimeStampAbstractModel
from apps.core.models.abstracts import UrlsMixin
from apps.core.utils import round_to_nearest
from apps.fin.models import Compensation
from apps.hr.models import Employee

from ..managers import VoucherTransactionManager
from .journal_entry import JournalEntry
from .voucher import Voucher


class VoucherTransaction(UrlsMixin, TimeStampAbstractModel, models.Model):
    uuid = models.UUIDField(
        editable=False,
        default=uuid.uuid4,
    )
    voucher = models.ForeignKey(
        Voucher,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name=_("voucher"),
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name=_("employee"),
    )
    compensation = models.ForeignKey(
        Compensation,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name=_("compensation"),
    )
    quantity = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name=_("quantity"),
        default=1,
    )
    value = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name=_("value"),
        default=0,
    )
    tax = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name=_("tax"),
        default=0,
    )
    notes = models.TextField(
        verbose_name=_("notes"),
        default="",
        blank=True,
    )
    ordering = models.PositiveIntegerField(
        default=0,
    )  # to order objects in inlines
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        allow_unicode=True,
    )

    objects: VoucherTransactionManager = VoucherTransactionManager()

    def calculate_compensation_value(self):
        return self.compensation.calculate(self.value, self.employee)

    def calculate_tax(self, value: Decimal | int | float | None = None):
        if value is None:
            value = self.calculate_compensation_value()

        if self.compensation.tax:
            tax_value = self.compensation.tax.calculate(value, rounded=False)
            tax = round_to_nearest(
                number=tax_value * self.quantity,
                method=self.compensation.tax.round_method,
                to_nearest=self.compensation.tax.rounded_to,
            )
        else:
            tax = Decimal(0)

        return tax

    def clean(self):
        errors: dict[str, ValidationError] = {}

        if (
            getattr(self, "compensation", None)
            and self.compensation.calculation_method
            == self.compensation.CalculationChoices.FORMULA
        ):
            try:
                self.compensation.calculate(self.value, self.employee)
            except FormulaNotValid as e:
                errors["compensation"] = ValidationError(
                    "the formula is not valid, REASON: {}".format(e.args[0]),
                )

        if getattr(self, "employee", None) and self.employee.status.is_payable is False:
            errors["employee"] = ValidationError(
                _("the employee ({}) is {}").format(
                    self.employee.fullname,
                    self.employee.status.name,
                )
            )

        if getattr(self, "compensation", None) and self.compensation.is_active is False:
            errors["compensation"] = ValidationError(
                _("the compensation ({}) is not active").format(self.compensation.name)
            )

        if (
            getattr(self, "compensation", None)
            and self.compensation.calculation_method
            == self.compensation.CalculationChoices.BY_INPUT
        ):
            if self.value < self.compensation.min_value:
                errors["value"] = ValidationError(
                    _(
                        "value must be greater than or equal to compensation min value ({:,.2f})"
                    ).format(self.compensation.min_value),
                )

            if self.value > self.compensation.max_value:
                errors["value"] = ValidationError(
                    _(
                        "value must be less than or equal to compensation max value ({:,.2f})"
                    ).format(self.compensation.max_value),
                )

        if errors:
            raise ValidationError(errors)

    def __migrate(
        self,
        calculate_for: Literal["tax", "compensation"] = "compensation",
    ):
        kwargs = {
            "date": self.voucher.date,
            "month": self.voucher.month,
            "quarter": self.voucher.quarter,
            "period": self.voucher.period,
            "employee": self.employee,
            "cost_center": self.employee.cost_center,
            "voucher": self.voucher,
            "notes": self.notes,
        }

        if calculate_for == "compensation":
            kwargs["content_type"] = ContentType.objects.get_for_model(
                self.compensation.__class__,
            )
            kwargs["fiscal_object_id"] = self.compensation.id

            amount = self.get_total()

            if amount < 0:
                kwargs["credit"] = abs(amount)
            else:
                kwargs["debit"] = amount

            kwargs["explanation"] = self.total_information

        else:
            kwargs["content_type"] = ContentType.objects.get_for_model(
                self.compensation.tax.__class__,
            )
            kwargs["fiscal_object_id"] = self.compensation.tax.id

            amount = self.tax

            if amount < 0:
                kwargs["debit"] = abs(amount)
            else:
                kwargs["credit"] = amount

            kwargs["explanation"] = self.tax_information

        JournalEntry.objects.create(**kwargs)

    def migrate(self):
        """Migrate the voucher transaction and generate a journal entry."""
        self.__migrate(calculate_for="compensation")

        if self.tax != 0:
            self.__migrate(calculate_for="tax")

    def get_total(self) -> Decimal:
        return self.quantity * self.value

    @property
    def total_information(self):
        if self.quantity == 1:
            return f"{self.compensation.name} - {self.value:,.2f}"
        return f"{self.quantity:,.2f} × {self.value:,.2f} {self.compensation.name}"

    @property
    def tax_information(self):
        result = 0
        if self.compensation.tax is None:
            return result

        if self.compensation.tax.fixed:
            tax_without_round = self.compensation.tax.rate * self.get_total()
            difference = self.tax - tax_without_round

            result = (
                f"{self.get_total():,.2f} × {self.compensation.tax.rate * 100:,.2f} %"
            )
            if difference < 0:
                result = f"({result})"
                result += f" - {difference:,.2f}"
            if difference > 0:
                result = f"({result})"
                result += f" + {difference:,.2f}"
        else:
            if self.quantity == 1:
                result = _("{} on {:,.2f}").format(
                    self.compensation.tax.name, self.value
                )
            else:
                result = _("{} on {:,.2f} ({:,.2f} × {:,.2f})").format(
                    self.compensation.tax.name,
                    self.value,
                    self.tax / self.quantity,
                    self.quantity,
                )

        return result

    @property
    def net_information(self):
        return f"[{self.total_information}] - [{self.tax_information}]"

    def __str__(self):
        return self.uuid.hex

    class Meta:
        icon = "circle-stack"
        ordering = ("-voucher__date", "voucher__voucher_serial", "ordering")
        codename_plural = "voucher_transactions"
        verbose_name = _("voucher transaction").title()
        verbose_name_plural = _("voucher transactions").title()
        permissions = (
            ("export_vouchertransaction", "Can export voucher transaction"),
            (
                "view_activity_vouchertransaction",
                "Can view voucher transaction activity",
            ),
        )


class ActivitySerializer(serializers.ModelSerializer):
    voucher = serializers.CharField(source="voucher.voucher_serial")
    compensation = serializers.CharField(source="compensation.name")
    employee = serializers.CharField(source="employee.fullname")

    class Meta:
        model = VoucherTransaction
        fields = (
            "voucher",
            "employee",
            "compensation",
            "quantity",
            "value",
            "notes",
        )


def slugify_voucher_transaction(
    sender,
    instance: VoucherTransaction,
    *args,
    **kwargs,
):
    if instance.slug is None:
        instance.slug = instance.uuid.hex


def pre_save_calculations(
    sender,
    instance: VoucherTransaction,
    *args,
    **kwargs,
):
    compensation_value = instance.calculate_compensation_value()
    instance.value = compensation_value
    instance.tax = instance.calculate_tax(compensation_value)


pre_save.connect(slugify_voucher_transaction, sender=VoucherTransaction)
pre_save.connect(pre_save_calculations, sender=VoucherTransaction)
pre_save.connect(
    signals.add_update_activity(ActivitySerializer), sender=VoucherTransaction
)
pre_delete.connect(
    signals.add_delete_activity(ActivitySerializer), sender=VoucherTransaction
)
