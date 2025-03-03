import django_filters
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from apps.core.filters import (
    BaseNameDescriptionFilter,
    BaseQSearchFilter,
    FilterComboboxMixin,
    get_combobox_choices_filter,
    get_number_from_to_filters,
    get_ordering_filter,
)
from apps.core.widgets import ComboboxWidget

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
    level_from, level_to = get_number_from_to_filters(field_name="level")

    def filter_kind(self, qs, name, value):
        if value == self.DepartmentKind.PARENT:
            return qs.filter(children__isnull=False).distinct()
        elif value == self.DepartmentKind.CHILD:
            return qs.filter(children__isnull=True).distinct()
        else:
            return qs

    def filter_parent(self, qs, name, value):
        if not value:
            return qs

        stmt = qs.none()
        for obj in value:
            stmt = obj.get_descendants() | stmt

        return stmt

    class Meta:
        model = models.Department
        fields = (
            "name",
            "parent",
            "kind",
            "level_from",
            "level_to",
            "cost_center",
            "description",
        )


class APIDepartmentFilter(FilterComboboxMixin, BaseDepartmentFilter):
    parent = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Department.objects.all(),
        field_name="parent",
        lookup_expr="in",
        label=_("parent"),
        method="filter_parent",
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
    parent = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Department.objects.all(),
        field_name="parent",
        lookup_expr="in",
        label=_("parent"),
        method="filter_parent",
        widget=ComboboxWidget({"data-name": _("parent")}),
    )
    cost_center = get_combobox_choices_filter(
        model=models.Department,
        field_name="cost_center__name",
        label=_("cost center"),
    )
