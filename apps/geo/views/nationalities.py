from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View, DetailView
from django.views.generic.list import MultipleObjectMixin
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.schemas import Action
from apps.core.utils import Deleter

from .. import filters, forms, models, resources, serializers
from ..constants import nationalities as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Nationality.objects.all()
    serializer_class = serializers.NationalitySerializer
    activity_serializer = serializers.NationalityActivitySerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APINationalityFilter
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
    permission_required = "geo.view_nationality"
    filter_class = filters.NationalityFilter
    resource_class = resources.NationalityResource
    activity_serializer = serializers.NationalityActivitySerializer
    deleter = Deleter
    search_fields = constants.SEARCH_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("geo.delete_nationality",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "geo.view_nationality"
    model = models.Nationality


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "geo.add_nationality"
    form_class = forms.NationalityForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "geo.change_nationality"
    form_class = forms.NationalityForm


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "geo.delete_nationality"
    deleter = Deleter
    activity_serializer = serializers.NationalityActivitySerializer
