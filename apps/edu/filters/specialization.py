import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_ordering_filter,
)

from .. import models
from ..constants import specialization as constants


class BaseSpecializationFilter(BaseNameDescriptionFilter):
    is_specialist = filters.ChoiceFilter(
        label=_("is specialist").title(),
        choices=models.Specialization.SpecialistChoices,
    )

    class Meta:
        model = models.Specialization
        fields = ("name", "is_specialist", "description")


class APISpecializationFilter(BaseSpecializationFilter):
    pass


class SpecializationFilter(
    BaseQSearchFilter,
    BaseSpecializationFilter,
):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
