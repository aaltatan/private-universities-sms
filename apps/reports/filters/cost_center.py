import django_filters as filters
from django.db import models
from django.utils.translation import gettext as _

from apps.core.filters import FilterTextMixin, get_text_filter
from apps.org.models import CostCenter

from .mixins import (
    CommonJournalsFilter,
    JournalsCompensationFilter,
    JournalsPeriodFilter,
)


class CostCenterFilter(
    FilterTextMixin,
    CommonJournalsFilter,
    JournalsCompensationFilter,
    JournalsPeriodFilter,
):
    name = get_text_filter(_("cost center name"))

    class Meta:
        model = CostCenter
        fields = ("name",)
        filter_overrides = {
            models.GeneratedField: {
                "filter_class": filters.CharFilter,
            },
        }
