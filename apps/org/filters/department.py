from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_ordering_filter,
)

from .. import models
from ..constants import departments as constants


class BaseDepartmentFilter(BaseNameDescriptionFilter):
    class Meta:
        model = models.Department
        fields = (
            "name",
            "cost_center",
            "description",
        )


class APIDepartmentFilter(FilterComboboxMixin, BaseDepartmentFilter):
    cost_center = get_combobox_choices_filter(
        model=models.Department,
        field_name="cost_center__name",
        label=_("cost center"),
        api_filter=True,
    )


class DepartmentFilter(
    FilterComboboxMixin,
    BaseQSearchFilter,
    BaseDepartmentFilter,
):
    ordering = get_ordering_filter(constants.ORDERING_FIELDS)
    cost_center = get_combobox_choices_filter(
        model=models.Department,
        field_name="cost_center__name",
        label=_("cost center"),
    )
