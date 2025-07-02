import django_filters as filters
from django.db.models import Q
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


class BaseJournalEntryFilter(FilterTextMixin, FilterComboboxMixin, filters.FilterSet):
    created_at_from, created_at_to = get_date_from_to_filters(
        "created_at",
    )
    updated_at_from, updated_at_to = get_date_from_to_filters(
        "updated_at",
    )
    date_from, date_to = get_date_from_to_filters("date")
    month = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="month",
        label=_("month"),
        choices=MonthChoices.choices,
    )
    quarter = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="quarter",
        label=_("quarter"),
        choices=QuarterChoices,
    )
    period = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="period__name",
        label=_("period"),
    )
    year = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="period__year__name",
        label=_("year"),
    )
    content_type = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="content_type__model",
        label=_("content type"),
    )
    fiscal_object = get_text_filter(
        method_name="filter_fiscal_object",
        label=_("fiscal object"),
        placeholder=_("e.g. fixed salary"),
    )
    debit_from, debit_to = get_number_from_to_filters("debit")
    credit_from, credit_to = get_number_from_to_filters("credit")
    employee = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="employee__fullname",
        label=_("employee"),
    )
    cost_center = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="cost_center__name",
        label=_("cost center"),
    )
    voucher = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="voucher__voucher_serial",
        label=_("voucher".title()),
    )
    explanation = get_text_filter(
        label=_("explanation".title()),
        field_name="explanation",
        placeholder=_("e.g. June 2025 Salaries"),
    )
    notes = get_text_filter(
        label=_("notes".title()),
        field_name="notes",
        placeholder=_("e.g. June 2025 Salaries"),
    )

    def filter_fiscal_object(self, queryset, name, value):
        return queryset.filter(
            Q(compensation__name__icontains=value) | Q(tax__name__icontains=value)
        )

    class Meta:
        model = models.JournalEntry
        fields = (
            "created_at_from",
            "created_at_to",
            "updated_at_from",
            "updated_at_to",
            "date_from",
            "date_to",
            "month",
            "quarter",
            "period",
            "debit_from",
            "debit_to",
            "content_type",
            "fiscal_object",
            "credit_from",
            "credit_to",
            "employee",
            "cost_center",
            "voucher",
            "explanation",
            "notes",
        )


class APIJournalEntryFilter(BaseJournalEntryFilter):
    period = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="period__name",
        label=_("period"),
        api_filter=True,
    )
    year = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="period__year__name",
        label=_("year"),
        api_filter=True,
    )
    content_type = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="content_type__model",
        label=_("content type"),
        api_filter=True,
    )
    employee = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="employee__fullname",
        label=_("employee"),
        api_filter=True,
    )
    cost_center = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="cost_center__name",
        label=_("cost center"),
        api_filter=True,
    )
    voucher = get_combobox_choices_filter(
        model=models.JournalEntry,
        field_name="voucher__voucher_serial",
        label=_("voucher".title()),
        api_filter=True,
    )


class JournalEntryFilter(BaseJournalEntryFilter):
    pass
