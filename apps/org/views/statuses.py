from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
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
    queryset = models.Status.objects.annotate_employees_count().all()
    serializer_class = serializers.StatusSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIStatusFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = Deleter


class ListView(PermissionRequiredMixin, mixins.ListMixin, View):
    permission_required = "org.view_status"
    model = models.Status
    filter_class = filters.StatusFilter
    resource_class = resources.StatusResource
    ordering_fields = constants.ORDERING_FIELDS

    def get_queryset(self):
        return models.Status.objects.annotate_employees_count().all()

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                behavior=Deleter,
                template="components/blocks/modals/bulk-delete.html",
                permissions=("org.delete_status",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "org.view_status"
    model = models.Status

    def get_queryset(self):
        return models.Status.objects.annotate_employees_count().all()


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "org.add_status"
    form_class = forms.StatusForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "org.change_status"
    form_class = forms.StatusForm


class DeleteView(PermissionRequiredMixin, mixins.BehaviorMixin, View):
    permission_required = "org.delete_status"
    behavior = Deleter
    model = models.Status
