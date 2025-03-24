from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
from django.views.generic.list import MultipleObjectMixin
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.schemas import Action
from apps.core.utils import Deleter

from .. import filters, forms, models, resources, serializers
from ..constants import cities as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APICitiesFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = Deleter

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return serializers.CreateUpdateCitySerializer
        return serializers.CitySerializer


class ListView(
    PermissionRequiredMixin,
    mixins.BulkDeleteMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required = "geo.view_city"
    model = models.City
    filter_class = filters.CityFilter
    resource_class = resources.CityResource
    deleter = Deleter
    ordering_fields = constants.ORDERING_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("geo.delete_city",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "geo.view_city"
    model = models.City


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "geo.add_city"
    form_class = forms.CityForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "geo.change_city"
    form_class = forms.CityForm


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "geo.delete_city"
    deleter = Deleter
    model = models.City
