import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import BaseNameDescriptionFilter, get_number_from_to_filters

from .. import models


class BaseStatusFilter(BaseNameDescriptionFilter):
    is_payable = filters.ChoiceFilter(
        label=_("payable"),
        choices=models.Status.PayableChoices,
    )
    is_separated = filters.ChoiceFilter(
        label=_("separated"),
        choices=models.Status.SeparatedChoices,
    )
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.Status
        fields = (
            "name",
            "is_payable",
            "is_separated",
            "employees_count_from",
            "employees_count_to",
            "description",
        )


class APIStatusFilter(BaseStatusFilter):
    pass


class StatusFilter(BaseStatusFilter):
    pass
