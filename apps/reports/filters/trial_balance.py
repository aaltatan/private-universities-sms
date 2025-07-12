import django_filters as filters
from django.db import models

from apps.core.filters import FilterTextMixin
from apps.hr.models import Employee


class TrialBalanceFilter(FilterTextMixin, filters.FilterSet):
    class Meta:
        model = Employee
        fields = ("fullname",)
        filter_overrides = {
            models.GeneratedField: {
                "filter_class": filters.CharFilter,
            },
        }
