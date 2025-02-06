from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views import View
from django.views.generic.list import MultipleObjectMixin
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.schemas import Action

from .. import filters, forms, models, resources, serializers
from ..constants import governorates as constants
from ..utils import governorates as utils


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Governorate.objects.all()
    serializer_class = serializers.GovernorateSerializer
    activity_serializer = serializers.GovernorateActivitySerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIGovernoratesFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = utils.Deleter


class ListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    mixins.BulkDeleteMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required = "geo.view_governorate"
    filter_class = filters.GovernorateFilter
    resource_class = resources.GovernorateResource
    activity_serializer = serializers.GovernorateActivitySerializer
    deleter = utils.Deleter
    search_fields = constants.SEARCH_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("geo.delete_governorate",),
            ),
        }


class CreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    mixins.CreateMixin,
    View,
):
    permission_required = "geo.create_governorate"
    form_class = forms.GovernorateForm


class UpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    mixins.UpdateMixin,
    View,
):
    permission_required = "geo.change_governorate"
    form_class = forms.GovernorateForm
    activity_serializer = serializers.GovernorateActivitySerializer


class DeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    mixins.DeleteMixin,
    View,
):
    permission_required = "geo.delete_governorate"
    deleter = utils.Deleter
    activity_serializer = serializers.GovernorateActivitySerializer
