import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import BaseNameDescriptionFilter, get_number_from_to_filters

from .. import models


class BaseNationalityFilter(BaseNameDescriptionFilter):
    is_local = filters.ChoiceFilter(
        label=_("locality"),
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


class NationalityFilter(BaseNationalityFilter):
    pass
