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
from ..constants import positions as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Position.objects.all()
    serializer_class = serializers.PositionSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIPositionFilter
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
    permission_required = "org.view_position"
    model = models.Position
    filter_class = filters.PositionFilter
    resource_class = resources.PositionResource
    deleter = Deleter
    ordering_fields = constants.ORDERING_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("org.delete_position",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "org.view_position"
    model = models.Position


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "org.add_position"
    form_class = forms.PositionForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "org.change_position"
    form_class = forms.PositionForm


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "org.delete_position"
    deleter = Deleter
    model = models.Position
