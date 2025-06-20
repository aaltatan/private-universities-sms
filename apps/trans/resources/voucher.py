from decimal import Decimal

from django.utils.translation import gettext as _
from import_export import fields, resources, widgets

from apps.core.resources import (
    DehydrateBooleanMixin,
    DehydrateChoicesMixin,
    SerialResourceMixin,
)

from .. import models


class VoucherResource(
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
    created_by = fields.Field(
        attribute="created_by__username",
        column_name=_("created by").title(),
    )
    updated_at = fields.Field(
        attribute="updated_at",
        column_name=_("updated at").title(),
    )
    updated_by = fields.Field(
        attribute="updated_by__username",
        column_name=_("updated by").title(),
    )
    uuid = fields.Field(
        attribute="uuid",
        column_name=_("uuid").title(),
    )
    voucher_serial = fields.Field(
        attribute="voucher_serial",
        column_name=_("voucher serial").title(),
    )
    title = fields.Field(
        attribute="title",
        column_name=_("title").title(),
    )
    date = fields.Field(
        attribute="date",
        column_name=_("date").title(),
    )
    kind = fields.Field(
        attribute="kind",
        column_name=_("kind").title(),
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
    total = fields.Field(
        attribute="total",
        column_name=_("total").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    transactions_count = fields.Field(
        attribute="total",
        column_name=_("transactions count").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    quantity_total = fields.Field(
        attribute="quantity_total",
        column_name=_("quantity total").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    value_total = fields.Field(
        attribute="value_total",
        column_name=_("value total").title(),
        widget=widgets.NumberWidget(coerce_to_string=False),
    )
    tax_total = fields.Field(
        attribute="tax_total",
        column_name=_("tax total").title(),
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
        attribute="serial_id",
        column_name=_("serial id").title(),
    )
    serial_date = fields.Field(
        attribute="serial_date",
        column_name=_("serial date").title(),
    )
    approve_date = fields.Field(
        attribute="approve_date",
        column_name=_("approve date").title(),
    )
    due_date = fields.Field(
        attribute="due_date",
        column_name=_("due date").title(),
    )
    accounting_journal_sequence = fields.Field(
        attribute="accounting_journal_sequence",
        column_name=_("accounting journal sequence").title(),
    )
    is_audited = fields.Field(
        attribute="is_audited",
        column_name=_("is audited").title(),
    )
    audited_by = fields.Field(
        attribute="audited_by__username",
        column_name=_("audited by").title(),
    )
    is_migrated = fields.Field(
        attribute="is_migrated",
        column_name=_("is migrated").title(),
    )
    slug = fields.Field(
        attribute="slug",
        column_name=_("slug").title(),
    )

    def dehydrate_is_audited(self, obj) -> bool:
        return self._dehydrate_boolean(obj.is_audited)

    def dehydrate_is_migrated(self, obj) -> bool:
        return self._dehydrate_boolean(obj.is_migrated)

    def dehydrate_month(self, obj) -> str:
        return self._dehydrate_choices(obj, "month")

    def dehydrate_quarter(self, obj) -> str:
        return self._dehydrate_choices(obj, "quarter")

    def dehydrate_total(self, obj) -> Decimal:
        return obj.total

    def dehydrate_transactions_count(self, obj) -> Decimal:
        return obj.transactions_count

    def dehydrate_quantity_total(self, obj) -> Decimal:
        return obj.quantity_total

    def dehydrate_value_total(self, obj) -> Decimal:
        return obj.value_total

    def dehydrate_tax_total(self, obj) -> Decimal:
        return obj.tax_total

    def dehydrate_net(self, obj) -> Decimal:
        return obj.net

    class Meta:
        model = models.Voucher
        fields = (
            "serial",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
            "uuid",
            "voucher_serial",
            "title",
            "date",
            "kind",
            "month",
            "quarter",
            "period",
            "total",
            "transactions_count",
            "quantity_total",
            "value_total",
            "tax_total",
            "net",
            "notes",
            "serial_id",
            "serial_date",
            "approve_date",
            "due_date",
            "accounting_journal_sequence",
            "is_audited",
            "audited_by",
            "is_migrated",
            "slug",
        )
