import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_ordering_filter,
    get_number_from_to_filters,
)

from .. import models
from ..constants import degrees as constants


class BaseDegreeFilter(BaseNameDescriptionFilter):
    is_academic = filters.ChoiceFilter(
        label=_("is academic").title(),
        choices=models.Degree.AcademicChoices,
    )
    order_from, order_to = get_number_from_to_filters(field_name="order")

    class Meta:
        model = models.Degree
        fields = (
            "name",
            "order",
            "is_academic",
            "description",
        )


class APIDegreeFilter(BaseDegreeFilter):
    pass


class DegreeFilter(BaseQSearchFilter, BaseDegreeFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
