from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.schemas import Action
from apps.core.utils import Deleter

from .. import filters, forms, models, resources, serializers
from ..constants import periods as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Period.objects.all()
    serializer_class = serializers.PeriodSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIPeriodFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = Deleter

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return serializers.CreateUpdatePeriodSerializer
        return serializers.PeriodSerializer


class ListView(PermissionRequiredMixin, mixins.ListMixin, View):
    permission_required = "fin.view_period"
    model = models.Period
    filter_class = filters.PeriodFilter
    resource_class = resources.PeriodResource
    ordering_fields = constants.ORDERING_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                behavior=Deleter,
                template="components/blocks/modals/bulk-delete.html",
                permissions=("fin.delete_period",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "fin.view_period"
    model = models.Period


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "fin.add_period"
    form_class = forms.PeriodForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "fin.change_period"
    form_class = forms.PeriodForm


class DeleteView(PermissionRequiredMixin, mixins.BehaviorMixin, View):
    permission_required = "fin.delete_period"
    behavior = Deleter
    model = models.Period
