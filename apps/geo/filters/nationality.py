import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_number_from_to_filters,
    get_ordering_filter,
)

from .. import models
from ..constants import nationalities as constants


class BaseNationalityFilter(BaseNameDescriptionFilter):
    is_local = filters.ChoiceFilter(
        label=_("locality").title(),
        choices=models.Nationality.LocalityChoices,
    )
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.Nationality
        fields = (
            "name",
            "is_local",
            "employees_count_from",
            "employees_count_to",
            "description",
        )


class APINationalityFilter(BaseNationalityFilter):
    pass


class NationalityFilter(BaseQSearchFilter, BaseNationalityFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
