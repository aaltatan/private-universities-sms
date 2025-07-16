from typing import Any, Protocol

import django_filters as filters
from django.db import models
from django.utils.translation import gettext as _

from apps.core.choices import MonthChoices
from apps.core.filters import (
    get_combobox_choices_filter,
    get_date_from_to_filters,
    get_number_from_to_filters,
)
from apps.fin.models import Compensation, Period, Year
from apps.org.models import CostCenter
from apps.trans.models import Voucher


class Queryset(Protocol):
    def annotate_journals_total_debit(
        self, sum_filter_Q: models.Q | None = None
    ) -> "Queryset": ...

    def annotate_journals_total_credit(
        self, sum_filter_Q: models.Q | None = None
    ) -> "Queryset": ...

    def annotate_journals_total_amount(
        self, sum_filter_Q: models.Q | None = None
    ) -> "Queryset": ...


class ExcludeZeroNet(models.TextChoices):
    EXCLUDE = "exclude", _("exclude").title()
    INCLUDE = "include", _("include").title()


class JournalsCompensationFilter(filters.FilterSet):
    compensation = get_combobox_choices_filter(
        queryset=Compensation.objects.filter(journals__isnull=False).distinct(),
        field_name="name",
        label=_("compensation"),
        method_name="filter_compensation",
    )

    def filter_compensation(self, queryset, name, value):
        return self.filter_journals("compensation__name__in", value, queryset)


class JournalsPeriodFilter(filters.FilterSet):
    period = get_combobox_choices_filter(
        queryset=Period.objects.filter(journals__isnull=False).distinct(),
        field_name="name",
        label=_("period"),
        method_name="filter_period",
    )

    def filter_period(self, queryset, name, value):
        return self.filter_journals("period__name__in", value, queryset)


class JournalsCostCenterFilter(filters.FilterSet):
    cost_center = get_combobox_choices_filter(
        queryset=CostCenter.objects.filter(journals__isnull=False).distinct(),
        field_name="cost_center",
        label=_("cost center"),
        method_name="filter_cost_center",
    )

    def filter_cost_center(self, queryset, name, value):
        return self.filter_journals("cost_center__name__in", value, queryset)


class CommonJournalsFilter(filters.FilterSet):
    _sum_filter_Q = models.Q()

    def _get_joined_sum_filter_Q(self, sum_filter_Q: models.Q):
        self._sum_filter_Q &= sum_filter_Q
        return self._sum_filter_Q

    def filter_journals(
        self,
        field: str,
        value: Any,
        queryset: Queryset,
    ):
        sum_filter_Q = self._get_joined_sum_filter_Q(
            models.Q(**{f"journals__{field}": value}) if value else models.Q(),
        )
        return (
            queryset.annotate_journals_total_debit(sum_filter_Q)
            .annotate_journals_total_credit(sum_filter_Q)
            .annotate_journals_total_amount(sum_filter_Q)
        )

    total_debit_from, total_debit_to = get_number_from_to_filters("total_debit")
    total_credit_from, total_credit_to = get_number_from_to_filters("total_credit")
    total_amount_from, total_amount_to = get_number_from_to_filters("total_amount")
    exclude_zero_net = filters.ChoiceFilter(
        choices=ExcludeZeroNet.choices,
        method="filter_exclude_zero_net",
        label=_("exclude zero net"),
    )

    def filter_exclude_zero_net(self, queryset: models.QuerySet, name, value):
        if value == ExcludeZeroNet.EXCLUDE:
            queryset = queryset.filter(~models.Q(total_amount=0))
        return queryset

    # journals internals filters
    date_from, date_to = get_date_from_to_filters(
        field_name="date",
        method_name_from="filter_date_from",
        method_name_to="filter_date_to",
    )

    def filter_date_from(self, queryset, name, value):
        return self.filter_journals("date__gte", value, queryset)

    def filter_date_to(self, queryset, name, value):
        return self.filter_journals("date__lte", value, queryset)

    voucher_serial = get_combobox_choices_filter(
        queryset=Voucher.objects.filter(is_deleted=False),
        field_name="voucher_serial",
        label=_("voucher"),
        method_name="filter_voucher_serial",
    )

    def filter_voucher_serial(self, queryset, name, value):
        return self.filter_journals("voucher__voucher_serial__in", value, queryset)

    year = get_combobox_choices_filter(
        queryset=Year.objects.all(),
        field_name="name",
        label=_("year"),
        method_name="filter_year",
    )

    def filter_year(self, queryset, name, value):
        return self.filter_journals("period__year__name__in", value, queryset)

    month = get_combobox_choices_filter(
        queryset=Voucher.objects.all(),
        field_name="month",
        label=_("month"),
        choices=MonthChoices.choices,
        method_name="filter_month",
    )

    def filter_month(self, queryset, name, value):
        return self.filter_journals("month__in", value, queryset)
