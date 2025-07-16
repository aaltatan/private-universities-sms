import django_filters as filters
from django.db import models
from django.utils.translation import gettext as _

from apps.core.filters import FilterTextMixin, get_text_filter
from apps.fin.models import Period

from .mixins import (
    CommonJournalsFilter,
    JournalsCompensationFilter,
    JournalsCostCenterFilter,
    JournalsEmployeeFilter,
)


class PeriodFilter(
    FilterTextMixin,
    CommonJournalsFilter,
    JournalsCompensationFilter,
    JournalsCostCenterFilter,
    JournalsEmployeeFilter,
):
    name = get_text_filter(_("cost center name"))

    class Meta:
        model = Period
        fields = ("name",)
        filter_overrides = {
            models.GeneratedField: {
                "filter_class": filters.CharFilter,
            },
        }
