from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    get_ordering_filter,
    get_text_filter,
)

from .. import models
from ..constants import cost_centers as constants


class BaseCostCenterFilter(BaseNameDescriptionFilter):
    accounting_id = get_text_filter(
        label=_("accounting id").title(),
        exact=True,
    )

    class Meta:
        model = models.CostCenter
        fields = ("name", "accounting_id", "description")


class APICostCenterFilter(BaseCostCenterFilter):
    pass


class CostCenterFilter(BaseQSearchFilter, BaseCostCenterFilter):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
