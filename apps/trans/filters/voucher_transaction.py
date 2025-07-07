import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.choices import MonthChoices, QuarterChoices
from apps.core.filters import (
    FilterComboboxMixin,
    FilterTextMixin,
    get_combobox_choices_filter,
    get_date_from_to_filters,
    get_number_from_to_filters,
    get_text_filter,
)

from .. import models


class BaseVoucherTransactionFilter(
    FilterTextMixin, FilterComboboxMixin, filters.FilterSet
):
    voucher = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.filter(voucher__is_deleted=False),
        field_name="voucher__voucher_serial",
        label=_("voucher".title()),
    )
    created_at_from, created_at_to = get_date_from_to_filters(
        "voucher__created_at",
    )
    updated_at_from, updated_at_to = get_date_from_to_filters(
        "voucher__updated_at",
    )
    date_from, date_to = get_date_from_to_filters("voucher__date")
    kind = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="voucher__kind__name",
        label=_("kind"),
    )
    month = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="voucher__month",
        label=_("month"),
        choices=MonthChoices.choices,
    )
    quarter = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="voucher__quarter",
        label=_("quarter"),
        choices=QuarterChoices,
    )
    period = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="voucher__period__name",
        label=_("period"),
    )
    employee = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="employee__fullname",
        label=_("employee"),
    )
    compensation = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="compensation__name",
        label=_("compensation"),
    )
    value_from, value_to = get_number_from_to_filters("value")
    quantity_from, quantity_to = get_number_from_to_filters("quantity")
    total_from, total_to = get_number_from_to_filters("total")
    tax_from, tax_to = get_number_from_to_filters("tax")
    net_from, net_to = get_number_from_to_filters("net")
    voucher_notes = get_text_filter(
        label=_("voucher notes".title()),
        field_name="voucher__notes",
    )
    voucher_title = get_text_filter(
        label=_("title".title()),
        field_name="voucher__title",
        placeholder=_("e.g. June 2025 Salaries"),
    )
    voucher_serial_id = get_text_filter(
        label=_("serial id".title()),
        field_name="voucher__serial_id",
        placeholder=_("e.g. VOC 0001"),
    )
    voucher_accounting_journal_sequence = get_text_filter(
        label=_("accounting journal sequence".title()),
        field_name="voucher__accounting_journal_sequence",
    )
    is_audited = filters.ChoiceFilter(
        field_name="voucher__is_audited",
        label=_("is audited".title()),
        choices=models.Voucher.AuditedChoices,
    )
    is_migrated = filters.ChoiceFilter(
        field_name="voucher__is_migrated",
        label=_("is migrated".title()),
        choices=models.Voucher.MigratedChoices,
    )

    class Meta:
        model = models.VoucherTransaction
        fields = (
            "voucher",
            "voucher_title",
            "created_at_from",
            "created_at_to",
            "updated_at_from",
            "updated_at_to",
            "date_from",
            "date_to",
            "employee",
            "compensation",
            "quantity_from",
            "quantity_to",
            "value_from",
            "value_to",
            "total_from",
            "total_to",
            "tax_from",
            "tax_to",
            "net_from",
            "net_to",
            "kind",
            "month",
            "quarter",
            "period",
            "notes",
            "voucher_notes",
            "voucher_accounting_journal_sequence",
            "is_audited",
            "is_migrated",
        )


class APIVoucherTransactionFilter(BaseVoucherTransactionFilter):
    voucher = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="voucher__voucher_serial",
        label=_("voucher".title()),
        api_filter=True,
    )
    employee = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="employee__fullname",
        label=_("employee"),
        api_filter=True,
    )
    compensation = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="compensation__name",
        label=_("compensation"),
        api_filter=True,
    )
    kind = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="voucher__kind__name",
        label=_("kind"),
        api_filter=True,
    )
    month = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="voucher__month",
        label=_("month"),
        choices=MonthChoices.choices,
        api_filter=True,
    )
    quarter = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="voucher__quarter",
        label=_("quarter"),
        choices=QuarterChoices.choices,
        api_filter=True,
    )
    period = get_combobox_choices_filter(
        queryset=models.VoucherTransaction.objects.all(),
        field_name="voucher__period__name",
        label=_("period"),
        api_filter=True,
    )


class VoucherTransactionFilter(BaseVoucherTransactionFilter):
    pass
