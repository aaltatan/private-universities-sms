import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_ordering_filter,
)

from .. import models
from ..constants import statuses as constants


class BaseStatusFilter(BaseNameDescriptionFilter):
    is_payable = filters.ChoiceFilter(
        label=_("payable").title(),
        choices=models.Status.PayableChoices,
    )

    class Meta:
        model = models.Status
        fields = ("name", "is_payable", "description")


class APIStatusFilter(BaseStatusFilter):
    pass


class StatusFilter(BaseQSearchFilter, BaseStatusFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
