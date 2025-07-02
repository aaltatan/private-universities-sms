from django.utils.translation import gettext as _
from import_export import fields, resources, widgets

from apps.core.resources import (
    DehydrateBooleanMixin,
    DehydrateChoicesMixin,
    SerialResourceMixin,
)

from .. import models


class VoucherTransactionResource(
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
        attribute="voucher__created_at",
        column_name=_("created at").title(),
    )
    created_by = fields.Field(
        attribute="voucher__created_by__username",
        column_name=_("created by").title(),
    )
    updated_at = fields.Field(
        attribute="voucher__updated_at",
        column_name=_("updated at").title(),
    )
    updated_by = fields.Field(
        attribute="voucher__updated_by__username",
        column_name=_("updated by").title(),
    )
    uuid = fields.Field(
        attribute="voucher__uuid",
        column_name=_("uuid").title(),
    )
    voucher_serial = fields.Field(
        attribute="voucher__voucher_serial",
        column_name=_("voucher serial").title(),
    )
    title = fields.Field(
        attribute="voucher__title",
        column_name=_("title").title(),
    )
    date = fields.Field(
        attribute="voucher__date",
        column_name=_("date").title(),
    )
    kind = fields.Field(
        attribute="voucher__kind",
        column_name=_("kind").title(),
    )
    month = fields.Field(
        attribute="voucher__month",
        column_name=_("month").title(),
    )
    quarter = fields.Field(
        attribute="voucher__quarter",
        column_name=_("quarter").title(),
    )
    period = fields.Field(
        attribute="voucher__period",
        column_name=_("period").title(),
    )
    voucher_notes = fields.Field(
        attribute="voucher__notes",
        column_name=_("notes").title(),
    )
    employee = fields.Field(
        attribute="employee__fullname",
        column_name=_("employee").title(),
    )
    compensation = fields.Field(
        attribute="compensation__name",
        column_name=_("compensation").title(),
    )
    quantity = fields.Field(
        attribute="quantity",
        column_name=_("quantity").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    value = fields.Field(
        attribute="value",
        column_name=_("value").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    total = fields.Field(
        attribute="total",
        column_name=_("total").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    tax = fields.Field(
        attribute="tax",
        column_name=_("tax").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    net = fields.Field(
        attribute="net",
        column_name=_("net").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    notes = fields.Field(
        attribute="notes",
        column_name=_("notes").title(),
    )
    serial_id = fields.Field(
        attribute="voucher__serial_id",
        column_name=_("serial id").title(),
    )
    serial_date = fields.Field(
        attribute="voucher__serial_date",
        column_name=_("serial date").title(),
    )
    approve_date = fields.Field(
        attribute="voucher__approve_date",
        column_name=_("approve date").title(),
    )
    due_date = fields.Field(
        attribute="voucher__due_date",
        column_name=_("due date").title(),
    )
    accounting_journal_sequence = fields.Field(
        attribute="voucher__accounting_journal_sequence",
        column_name=_("accounting journal sequence").title(),
    )
    is_audited = fields.Field(
        attribute="voucher__is_audited",
        column_name=_("is audited").title(),
    )
    audited_by = fields.Field(
        attribute="voucher__audited_by__username",
        column_name=_("audited by").title(),
    )
    is_migrated = fields.Field(
        attribute="voucher__is_migrated",
        column_name=_("is migrated").title(),
    )

    def dehydrate_is_audited(self, obj) -> bool:
        return self._dehydrate_boolean(obj.voucher.is_audited)

    def dehydrate_is_migrated(self, obj) -> bool:
        return self._dehydrate_boolean(obj.voucher.is_migrated)

    def dehydrate_month(self, obj) -> str:
        return self._dehydrate_choices(obj.voucher, "month")

    def dehydrate_quarter(self, obj) -> str:
        return self._dehydrate_choices(obj.voucher, "quarter")

    class Meta:
        model = models.Voucher
        fields = (
            "serial",
            "voucher_serial",
            "title",
            "date",
            "employee",
            "compensation",
            "quantity",
            "value",
            "total",
            "tax",
            "net",
            "notes",
            "kind",
            "month",
            "quarter",
            "period",
            "serial_id",
            "serial_date",
            "approve_date",
            "due_date",
            "accounting_journal_sequence",
            "voucher_notes",
            "is_audited",
            "audited_by",
            "is_migrated",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
            "uuid",
        )
