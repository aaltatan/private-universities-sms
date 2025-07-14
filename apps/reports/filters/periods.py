from typing import Any

import django_filters as filters
from django.db import models
from django.utils.translation import gettext as _

from apps.core.choices import MonthChoices
from apps.core.filters import (
    FilterTextMixin,
    get_combobox_choices_filter,
    get_date_from_to_filters,
    get_number_from_to_filters,
    get_text_filter,
)
from apps.fin.models import Year
from apps.fin.models import Period, PeriodQuerySet
from apps.trans.models import Voucher


class ExcludeZeroNet(models.TextChoices):
    EXCLUDE = "exclude", _("exclude").title()
    INCLUDE = "include", _("include").title()


class FilterJournalsMixin:
    _sum_filter_Q = models.Q()

    def _get_joined_sum_filter_Q(self, sum_filter_Q: models.Q):
        self._sum_filter_Q &= sum_filter_Q
        return self._sum_filter_Q

    def filter_journals(
        self,
        field: str,
        value: Any,
        queryset: PeriodQuerySet,
    ):
        sum_filter_Q = self._get_joined_sum_filter_Q(
            models.Q(**{f"journals__{field}": value}),
        )
        return (
            queryset.annotate_journals_total_debit(sum_filter_Q)
            .annotate_journals_total_credit(sum_filter_Q)
            .annotate_journals_total_amount(sum_filter_Q)
        )


class PeriodFilter(
    FilterJournalsMixin,
    FilterTextMixin,
    filters.FilterSet,
):
    name = get_text_filter(_("cost center name"))
    total_debit_from, total_debit_to = get_number_from_to_filters("total_debit")
    total_credit_from, total_credit_to = get_number_from_to_filters("total_credit")
    total_amount_from, total_amount_to = get_number_from_to_filters("total_amount")
    exclude_zero_net = filters.ChoiceFilter(
        choices=ExcludeZeroNet.choices,
        method="filter_exclude_zero_net",
        label=_("exclude zero net"),
    )

    # journals internals filters
    date_from, date_to = get_date_from_to_filters(
        field_name="date",
        method_name_from="filter_date_from",
        method_name_to="filter_date_to",
    )
    voucher_serial = get_combobox_choices_filter(
        queryset=Voucher.objects.filter(is_deleted=False),
        field_name="voucher_serial",
        label=_("voucher"),
        method_name="filter_voucher_serial",
    )
    year = get_combobox_choices_filter(
        queryset=Year.objects.all(),
        field_name="name",
        label=_("year"),
        method_name="filter_year",
    )
    month = get_combobox_choices_filter(
        queryset=Voucher.objects.all(),
        field_name="month",
        label=_("month"),
        choices=MonthChoices.choices,
        method_name="filter_month",
    )

    def filter_exclude_zero_net(self, queryset: PeriodQuerySet, name, value):
        if value == ExcludeZeroNet.EXCLUDE:
            queryset = queryset.filter(~models.Q(total_amount=0))
        return queryset

    def filter_voucher_serial(self, queryset: PeriodQuerySet, name, value):
        return self.filter_journals("voucher__voucher_serial__in", value, queryset)

    def filter_month(self, queryset: PeriodQuerySet, name, value):
        return self.filter_journals("month__in", value, queryset)

    def filter_year(self, queryset: PeriodQuerySet, name, value):
        return self.filter_journals("period__year__name__in", value, queryset)

    def filter_date_from(self, queryset: PeriodQuerySet, name, value):
        return self.filter_journals("date__gte", value, queryset)

    def filter_date_to(self, queryset: PeriodQuerySet, name, value):
        return self.filter_journals("date__lte", value, queryset)

    class Meta:
        model = Period
        fields = (
            "name",
            "voucher_serial",
            "year",
            "month",
        )
        filter_overrides = {
            models.GeneratedField: {
                "filter_class": filters.CharFilter,
            },
        }
