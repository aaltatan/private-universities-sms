from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.views.generic.list import MultipleObjectMixin
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.schemas import Action
from apps.core.utils import Deleter

from .. import filters, forms, models, resources, serializers
from ..constants import statuses as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    activity_serializer = serializers.StatusActivitySerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIStatusFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = Deleter


class ListView(
    PermissionRequiredMixin,
    mixins.BulkDeleteMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required = "org.view_status"
    filter_class = filters.StatusFilter
    resource_class = resources.StatusResource
    activity_serializer = serializers.StatusActivitySerializer
    deleter = Deleter
    search_fields = constants.SEARCH_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("org.delete_status",),
            ),
        }


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "org.add_status"
    form_class = forms.StatusForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "org.change_status"
    form_class = forms.StatusForm
    activity_serializer = serializers.StatusActivitySerializer


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "org.delete_status"
    deleter = Deleter
    activity_serializer = serializers.StatusActivitySerializer
