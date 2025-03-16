import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_number_from_to_filters,
    get_ordering_filter,
)

from .. import models
from ..constants import specialization as constants


class BaseSpecializationFilter(BaseNameDescriptionFilter):
    is_specialist = filters.ChoiceFilter(
        label=_("is specialist").title(),
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


class SpecializationFilter(
    BaseQSearchFilter,
    BaseSpecializationFilter,
):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
