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
from apps.core.schemas import Action, Perm

from . import constants, filters, forms, models, resources, serializers, utils


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    activity_serializer = serializers.ActivitySerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APICitiesFilter
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
    permission_required: str = Perm("cities").string
    filter_class = filters.CityFilter
    resource_class = resources.CityResource
    activity_serializer = serializers.ActivitySerializer
    deleter = utils.Deleter
    search_fields = constants.SEARCH_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=(Perm("cities", "delete"),),
            ),
        }


class CreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    mixins.CreateMixin,
    View,
):
    permission_required: str = Perm("cities", "add").string
    form_class = forms.CityForm


class UpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    mixins.UpdateMixin,
    View,
):
    permission_required: str = Perm("cities", "change").string
    form_class = forms.CityForm
    activity_serializer = serializers.ActivitySerializer


class DeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    mixins.DeleteMixin,
    View,
):
    permission_required: str = Perm("cities", "delete").string
    deleter = utils.Deleter
    activity_serializer = serializers.ActivitySerializer
