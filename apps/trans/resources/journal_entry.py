from django.utils.translation import gettext as _
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
        column_name=_("created at").title(),
    )
    updated_at = fields.Field(
        attribute="updated_at",
        column_name=_("updated at").title(),
    )
    uuid = fields.Field(
        attribute="uuid",
        column_name=_("uuid").title(),
    )
    date = fields.Field(
        attribute="date",
        column_name=_("date").title(),
    )
    month = fields.Field(
        attribute="month",
        column_name=_("month").title(),
    )
    quarter = fields.Field(
        attribute="quarter",
        column_name=_("quarter").title(),
    )
    period = fields.Field(
        attribute="period",
        column_name=_("period").title(),
    )
    year = fields.Field(
        attribute="period__year",
        column_name=_("year").title(),
    )
    employee = fields.Field(
        attribute="employee__fullname",
        column_name=_("employee").title(),
    )
    cost_center = fields.Field(
        attribute="cost_center__name",
        column_name=_("cost center").title(),
    )
    fiscal_object = fields.Field(
        column_name=_("fiscal object").title(),
        dehydrate_method="dehydrate_fiscal_object",
    )
    debit = fields.Field(
        attribute="debit",
        column_name=_("debit").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    credit = fields.Field(
        attribute="credit",
        column_name=_("credit").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    net = fields.Field(
        attribute="net",
        column_name=_("net").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    explanation = fields.Field(
        attribute="explanation",
        column_name=_("explanation").title(),
    )
    notes = fields.Field(
        attribute="notes",
        column_name=_("notes").title(),
    )
    voucher_serial = fields.Field(
        column_name=_("voucher serial").title(),
        dehydrate_method="dehydrate_voucher_serial",
    )
    voucher_title = fields.Field(
        column_name=_("voucher title").title(),
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
