import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import BaseNameDescriptionFilter, get_number_from_to_filters

from .. import models


class BaseDegreeFilter(BaseNameDescriptionFilter):
    is_academic = filters.ChoiceFilter(
        label=_("is academic").title(),
        choices=models.Degree.AcademicChoices,
    )
    order_from, order_to = get_number_from_to_filters(field_name="order")
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.Degree
        fields = (
            "name",
            "order_from",
            "order_to",
            "employees_count_from",
            "employees_count_to",
            "is_academic",
            "description",
        )


class APIDegreeFilter(BaseDegreeFilter):
    pass


class DegreeFilter(BaseDegreeFilter):
    pass
