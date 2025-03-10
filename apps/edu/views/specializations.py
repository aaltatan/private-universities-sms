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
from ..constants import specialization as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Specialization.objects.all()
    serializer_class = serializers.SpecializationSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APISpecializationFilter
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
    permission_required = "edu.view_specialization"
    filter_class = filters.SpecializationFilter
    resource_class = resources.SpecializationResource
    deleter = Deleter
    search_fields = constants.SEARCH_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("edu.delete_specialization",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "edu.view_specialization"
    model = models.Specialization


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "edu.add_specialization"
    form_class = forms.SpecializationForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "edu.change_specialization"
    form_class = forms.SpecializationForm


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "edu.delete_specialization"
    deleter = Deleter
    model = models.Specialization
