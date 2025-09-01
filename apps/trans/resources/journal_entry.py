from django.utils.translation import gettext_lazy as _
from import_export import fields, resources, widgets

from apps.core.resources import (
    DehydrateBooleanMixin,
    DehydrateChoicesMixin,
    SerialResourceMixin,
)

from .. import models


class JournalEntryResource(
    SerialResourceMixin,
    DehydrateChoicesMixin,
    DehydrateBooleanMixin,
    resources.ModelResource,
):
    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    created_at = fields.Field(
        attribute="created_at",
        column_name=_("created at"),
    )
    updated_at = fields.Field(
        attribute="updated_at",
        column_name=_("updated at"),
    )
    uuid = fields.Field(
        attribute="uuid",
        column_name=_("uuid"),
    )
    date = fields.Field(
        attribute="date",
        column_name=_("date"),
    )
    month = fields.Field(
        attribute="month",
        column_name=_("month"),
    )
    quarter = fields.Field(
        attribute="quarter",
        column_name=_("quarter"),
    )
    period = fields.Field(
        attribute="period",
        column_name=_("period"),
    )
    year = fields.Field(
        attribute="period__year",
        column_name=_("year"),
    )
    employee_uuid = fields.Field(
        attribute="employee__uuid",
        column_name=_("employee uuid"),
    )
    employee = fields.Field(
        attribute="employee__fullname",
        column_name=_("employee"),
    )
    cost_center = fields.Field(
        attribute="cost_center__name",
        column_name=_("cost center"),
    )
    fiscal_object = fields.Field(
        column_name=_("fiscal object"),
        dehydrate_method="dehydrate_fiscal_object",
    )
    debit = fields.Field(
        attribute="debit",
        column_name=_("debit"),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    credit = fields.Field(
        attribute="credit",
        column_name=_("credit"),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    net = fields.Field(
        attribute="net",
        column_name=_("net"),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    explanation = fields.Field(
        attribute="explanation",
        column_name=_("explanation"),
    )
    notes = fields.Field(
        attribute="notes",
        column_name=_("notes"),
    )
    voucher_serial = fields.Field(
        column_name=_("voucher serial"),
        dehydrate_method="dehydrate_voucher_serial",
    )
    voucher_title = fields.Field(
        column_name=_("voucher title"),
        dehydrate_method="dehydrate_voucher_title",
    )

    def dehydrate_voucher_serial(self, obj) -> str:
        if getattr(obj, "voucher", None) is None:
            return "-"
        return obj.voucher.voucher_serial

    def dehydrate_voucher_title(self, obj) -> str:
        if getattr(obj, "voucher", None) is None:
            return "-"
        return obj.voucher.title

    def dehydrate_fiscal_object(self, obj) -> str:
        return obj.fiscal_object.name

    def dehydrate_month(self, obj) -> str:
        return self._dehydrate_choices(obj.voucher, "month")

    def dehydrate_quarter(self, obj) -> str:
        return self._dehydrate_choices(obj.voucher, "quarter")

    class Meta:
        model = models.JournalEntry
        fields = (
            "serial",
            "debit",
            "credit",
            "net",
            "employee_uuid",
            "employee",
            "fiscal_object",
            "explanation",
            "cost_center",
            "voucher_serial",
            "voucher_title",
            "date",
            "year",
            "period",
            "month",
            "quarter",
            "notes",
            "created_at",
            "updated_at",
            "uuid",
        )
