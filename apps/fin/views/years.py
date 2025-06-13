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
from ..constants import years as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Year.objects.all()
    serializer_class = serializers.YearSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIYearFilter
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
    permission_required = "fin.view_year"
    model = models.Year
    filter_class = filters.YearFilter
    resource_class = resources.YearResource
    deleter = Deleter
    ordering_fields = constants.ORDERING_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("fin.delete_year",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "fin.view_year"
    model = models.Year


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "fin.add_year"
    form_class = forms.YearForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "fin.change_year"
    form_class = forms.YearForm


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "fin.delete_year"
    deleter = Deleter
    model = models.Year
