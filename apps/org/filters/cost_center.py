from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    get_number_from_to_filters,
    get_text_filter,
)

from .. import models


class BaseCostCenterFilter(BaseNameDescriptionFilter):
    accounting_id = get_text_filter(
        label=_("accounting id"),
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


class CostCenterFilter(BaseCostCenterFilter):
    pass
