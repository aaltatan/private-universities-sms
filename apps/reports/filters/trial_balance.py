from typing import Any

import django_filters as filters
from django.db import models
from django.utils.translation import gettext as _

from apps.core.filters import (
    FilterTextMixin,
    get_combobox_choices_filter,
    get_text_filter,
)
from apps.core.choices import MonthChoices
from apps.hr.models import Employee
from apps.hr.querysets import EmployeeQuerySet
from apps.org.models import CostCenter
from apps.trans.models import Voucher
from apps.fin.models import Period, Year


class FilterJournalsMixin:
    _sum_filter_Q = models.Q()

    def _get_joined_sum_filter_Q(self, sum_filter_Q: models.Q):
        self._sum_filter_Q &= sum_filter_Q
        return self._sum_filter_Q

    def filter_journals(
        self,
        field: str,
        value: Any,
        queryset: EmployeeQuerySet,
    ):
        sum_filter_Q = self._get_joined_sum_filter_Q(
            models.Q(**{f"journals__{field}": value}),
        )
        return queryset.annotate_journals_totals(sum_filter_Q)


class TrialBalanceFilter(
    FilterJournalsMixin,
    FilterTextMixin,
    filters.FilterSet,
):
    fullname = get_text_filter(_("employee fullname"))

    # journals internals filters
    voucher_serial = get_combobox_choices_filter(
        queryset=Voucher.objects.filter(is_deleted=False),
        field_name="voucher_serial",
        label=_("voucher"),
        method_name="filter_voucher_serial",
    )
    cost_center = get_combobox_choices_filter(
        queryset=CostCenter.objects.all(),
        field_name="name",
        label=_("cost center"),
        method_name="filter_cost_center",
    )
    year = get_combobox_choices_filter(
        queryset=Year.objects.all(),
        field_name="name",
        label=_("year"),
        method_name="filter_year",
    )
    period = get_combobox_choices_filter(
        queryset=Period.objects.all(),
        field_name="name",
        label=_("period"),
        method_name="filter_period",
    )
    month = get_combobox_choices_filter(
        queryset=Voucher.objects.all(),
        field_name="month",
        label=_("month"),
        choices=MonthChoices.choices,
        method_name="filter_month",
    )

    def filter_voucher_serial(self, queryset: EmployeeQuerySet, name, value):
        return self.filter_journals("voucher__voucher_serial__in", value, queryset)

    def filter_cost_center(self, queryset: EmployeeQuerySet, name, value):
        return self.filter_journals("cost_center__name__in", value, queryset)

    def filter_month(self, queryset: EmployeeQuerySet, name, value):
        return self.filter_journals("month__in", value, queryset)

    def filter_year(self, queryset: EmployeeQuerySet, name, value):
        return self.filter_journals("period__year__name__in", value, queryset)

    def filter_period(self, queryset: EmployeeQuerySet, name, value):
        return self.filter_journals("period__name__in", value, queryset)

    class Meta:
        model = Employee
        fields = (
            "fullname",
            "voucher_serial",
            "cost_center",
            "year",
            "period",
            "month",
        )
        filter_overrides = {
            models.GeneratedField: {
                "filter_class": filters.CharFilter,
            },
        }
