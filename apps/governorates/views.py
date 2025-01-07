from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import QuerySet
from django.views import View
from django.views.generic.list import MultipleObjectMixin

from apps.core.mixins import (
    BulkDeleteMixin,
    CreateMixin,
    DeleteMixin,
    ListMixin,
    UpdateMixin,
)
from apps.core.utils import Action, Deleter, Perm

from . import filters, forms, models, resources


class GovernorateDeleter(Deleter):
    def is_obj_deletable(self) -> bool:
        return True

    def is_qs_deletable(self, qs: QuerySet) -> bool:
        return True


class ListView(
    PermissionRequiredMixin,
    BulkDeleteMixin,
    ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required: str = Perm("governorates").string
    filter_class = filters.GovernorateFilter
    resource_class = resources.GovernorateResource
    deleter = GovernorateDeleter
    search_fields = "name", "description"

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=(Perm("governorates", "delete"),),
            ),
        }


class CreateView(PermissionRequiredMixin, CreateMixin, View):
    permission_required: str = Perm("governorates", "add").string
    form_class = forms.GovernorateForm


class UpdateView(PermissionRequiredMixin, UpdateMixin, View):
    permission_required: str = Perm("governorates", "change").string
    form_class = forms.GovernorateForm


class DeleteView(PermissionRequiredMixin, DeleteMixin, View):
    permission_required: str = Perm("governorates", "delete").string
    model = models.Governorate
    deleter = GovernorateDeleter