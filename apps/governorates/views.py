from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views import View
from django.views.generic.list import MultipleObjectMixin
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.utils import Action, Perm

from . import constants, filters, forms, models, resources, serializers, utils


class GovernorateViewSet(
    mixins.DestroyMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Governorate.objects.all()
    serializer_class = serializers.GovernorateSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        rest_filters.OrderingFilter,
    ]
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = utils.GovernorateDeleter


class ListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    mixins.BulkDeleteMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required: str = Perm("governorates").string
    filter_class = filters.GovernorateFilter
    resource_class = resources.GovernorateResource
    deleter = utils.GovernorateDeleter
    search_fields = constants.SEARCH_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=(Perm("governorates", "delete"),),
            ),
        }


class CreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    mixins.CreateMixin,
    View,
):
    permission_required: str = Perm("governorates", "add").string
    form_class = forms.GovernorateForm


class UpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    mixins.UpdateMixin,
    View,
):
    permission_required: str = Perm("governorates", "change").string
    form_class = forms.GovernorateForm


class DeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    mixins.DeleteMixin,
    View,
):
    permission_required: str = Perm("governorates", "delete").string
    model = models.Governorate
    deleter = utils.GovernorateDeleter
