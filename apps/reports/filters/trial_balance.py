import django_filters as filters
from django.db import models
from django.utils.translation import gettext as _

from apps.core.filters import FilterTextMixin, get_text_filter
from apps.hr.models import Employee

from .mixins import (
    CommonJournalsFilter,
    JournalsCompensationFilter,
    JournalsCostCenterFilter,
    JournalsPeriodFilter,
)


class TrialBalanceFilter(
    FilterTextMixin,
    CommonJournalsFilter,
    JournalsCompensationFilter,
    JournalsCostCenterFilter,
    JournalsPeriodFilter,
):
    filter_compensations = False
    fullname = get_text_filter(_("employee fullname"))

    class Meta:
        model = Employee
        fields = ("fullname",)
        filter_overrides = {
            models.GeneratedField: {
                "filter_class": filters.CharFilter,
            },
        }
