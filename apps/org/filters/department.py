import django_filters
from django.db.models import TextChoices
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
    class DepartmentKind(TextChoices):
        PARENT = "parent", _("parent").title()
        CHILD = "child", _("child").title()

    kind = django_filters.ChoiceFilter(
        choices=DepartmentKind,
        label=_("kind"),
        method="filter_kind",
    )

    def filter_kind(self, qs, name, value):
        if value == self.DepartmentKind.PARENT:
            return qs.filter(children__isnull=False).distinct()
        elif value == self.DepartmentKind.CHILD:
            return qs.filter(children__isnull=True).distinct()
        else:
            return qs

    class Meta:
        model = models.Department
        fields = ("name", "parent", "kind", "cost_center", "description")


class APIDepartmentFilter(FilterComboboxMixin, BaseDepartmentFilter):
    parent = get_combobox_choices_filter(
        model=models.Department,
        field_name="parent_department",
        label=_("parent"),
        api_filter=True,
    )
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
    parent = get_combobox_choices_filter(
        model=models.Department,
        field_name="parent_department",
        label=_("parent"),
    )
    cost_center = get_combobox_choices_filter(
        model=models.Department,
        field_name="cost_center__name",
        label=_("cost center"),
    )
