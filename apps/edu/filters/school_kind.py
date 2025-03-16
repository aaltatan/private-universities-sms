import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_ordering_filter,
    get_number_from_to_filters,
)

from .. import models
from ..constants import school_kinds as constants


class BaseSchoolKindFilter(BaseNameDescriptionFilter):
    is_governmental = filters.ChoiceFilter(
        label=_("is governmental").title(),
        choices=models.SchoolKind.OwnershipChoices,
    )
    is_virtual = filters.ChoiceFilter(
        label=_("is virtual").title(),
        choices=models.SchoolKind.VirtualChoices,
    )
    schools_count_from, schools_count_to = get_number_from_to_filters("schools_count")
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.SchoolKind
        fields = (
            "name",
            "is_governmental",
            "schools_count_from",
            "schools_count_to",
            "employees_count_from",
            "employees_count_to",
            "is_virtual",
            "description",
        )


class APISchoolKindFilter(BaseSchoolKindFilter):
    pass


class SchoolKindFilter(
    BaseQSearchFilter,
    BaseSchoolKindFilter,
):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
