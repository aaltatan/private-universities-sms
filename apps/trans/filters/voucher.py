import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.choices import MonthChoices, QuarterChoices
from apps.core.filters import (
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_date_from_to_filters,
    get_number_from_to_filters,
)
from apps.fin.models import Period

from .. import models


class BaseVoucherFilter(FilterComboboxMixin, filters.FilterSet):
    created_at_from, created_at_to = get_date_from_to_filters("created_at")
    updated_at_from, updated_at_to = get_date_from_to_filters("updated_at")
    date_from, date_to = get_date_from_to_filters("date")
    kind = get_combobox_choices_filter(
        model=models.Voucher,
        field_name="kind__name",
        label=_("kind"),
    )
    month = get_combobox_choices_filter(
        model=models.Voucher,
        field_name="month",
        label=_("month"),
        choices=MonthChoices.choices,
    )
    quarter = get_combobox_choices_filter(
        model=models.Voucher,
        field_name="quarter",
        label=_("quarter"),
        choices=QuarterChoices.choices,
    )
    period = get_combobox_choices_filter(
        model=models.Voucher,
        field_name="period__name",
        label=_("period"),
    )
    is_closed_period = filters.ChoiceFilter(
        field_name="period__is_closed",
        label=_("is closed period"),
        choices=Period.ClosedChoices.choices,
    )
    serial_date_from, serial_date_to = get_date_from_to_filters("serial_date")
    approve_date_from, approve_date_to = get_date_from_to_filters(
        "approve_date",
    )
    due_date_from, due_date_to = get_date_from_to_filters("due_date")
    transactions_count_from, transactions_count_to = get_number_from_to_filters(
        "transactions_count",
    )
    total_from, total_to = get_number_from_to_filters("total")
    net_from, net_to = get_number_from_to_filters("net")

    class Meta:
        model = models.Voucher
        fields = (
            "voucher_serial",
            "title",
            "created_at_from",
            "created_at_to",
            "updated_at_from",
            "updated_at_to",
            "date_from",
            "date_to",
            "transactions_count_from",
            "transactions_count_to",
            "total_from",
            "total_to",
            "net_from",
            "net_to",
            "kind",
            "month",
            "quarter",
            "period",
            "is_closed_period",
            "notes",
            "serial_id",
            "serial_date_from",
            "serial_date_to",
            "approve_date_from",
            "approve_date_to",
            "due_date_from",
            "due_date_to",
            "accounting_journal_sequence",
            "is_audited",
            "is_migrated",
        )


class APIVoucherFilter(BaseVoucherFilter):
    kind = get_combobox_choices_filter(
        model=models.Voucher,
        field_name="kind__name",
        label=_("kind"),
        api_filter=True,
    )
    month = get_combobox_choices_filter(
        model=models.Voucher,
        field_name="month",
        label=_("month"),
        choices=MonthChoices.choices,
        api_filter=True,
    )
    quarter = get_combobox_choices_filter(
        model=models.Voucher,
        field_name="quarter",
        label=_("quarter"),
        choices=QuarterChoices.choices,
        api_filter=True,
    )
    period = get_combobox_choices_filter(
        model=models.Voucher,
        field_name="period__name",
        label=_("period"),
        api_filter=True,
    )


class VoucherFilter(BaseVoucherFilter):
    pass
