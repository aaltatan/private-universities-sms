import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import BaseNameDescriptionFilter, get_number_from_to_filters

from .. import models


class BaseSpecializationFilter(BaseNameDescriptionFilter):
    is_specialist = filters.ChoiceFilter(
        label=_("is specialist"),
        choices=models.Specialization.SpecialistChoices,
    )
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.Specialization
        fields = (
            "name",
            "is_specialist",
            "description",
            "employees_count_from",
            "employees_count_to",
        )


class APISpecializationFilter(BaseSpecializationFilter):
    pass


class SpecializationFilter(BaseSpecializationFilter):
    pass
