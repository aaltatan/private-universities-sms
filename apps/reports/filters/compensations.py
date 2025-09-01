import django_filters as filters
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.filters import FilterTextMixin, get_text_filter
from apps.fin.models import Period

from .mixins import (
    CommonJournalsFilter,
    JournalsCostCenterFilter,
    JournalsEmployeeFilter,
    JournalsPeriodFilter,
)


class CompensationFilter(
    FilterTextMixin,
    CommonJournalsFilter,
    JournalsPeriodFilter,
    JournalsEmployeeFilter,
    JournalsCostCenterFilter,
):
    name = get_text_filter(_("compensation name"))

    class Meta:
        model = Period
        fields = ("name",)
        filter_overrides = {
            models.GeneratedField: {
                "filter_class": filters.CharFilter,
            },
        }
