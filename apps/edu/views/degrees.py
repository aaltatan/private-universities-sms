from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.schemas import Action
from apps.core.utils import Deleter

from .. import filters, forms, models, resources, serializers
from ..constants import degrees as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Degree.objects.all()
    serializer_class = serializers.DegreeSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIDegreeFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = Deleter


class ListView(PermissionRequiredMixin, mixins.ListMixin, View):
    permission_required = "edu.view_degree"
    model = models.Degree
    filter_class = filters.DegreeFilter
    resource_class = resources.DegreeResource
    ordering_fields = constants.ORDERING_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                behavior=Deleter,
                template="components/blocks/modals/bulk-delete.html",
                permissions=("edu.delete_degree",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "edu.view_degree"
    model = models.Degree


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "edu.add_degree"
    form_class = forms.DegreeForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "edu.change_degree"
    form_class = forms.DegreeForm


class DeleteView(PermissionRequiredMixin, mixins.BehaviorMixin, View):
    permission_required = "edu.delete_degree"
    behavior = Deleter
    model = models.Degree
