from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_ordering_filter,
    get_text_filter,
    get_number_from_to_filters,
)

from .. import models
from ..constants import cost_centers as constants


class BaseCostCenterFilter(BaseNameDescriptionFilter):
    accounting_id = get_text_filter(
        label=_("accounting id").title(),
        exact=True,
    )
    employees_count_from, employees_count_to = get_number_from_to_filters(
        "employees_count",
    )

    class Meta:
        model = models.CostCenter
        fields = (
            "name",
            "accounting_id",
            "employees_count_from",
            "employees_count_to",
            "description",
        )


class APICostCenterFilter(BaseCostCenterFilter):
    pass


class CostCenterFilter(BaseQSearchFilter, BaseCostCenterFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
