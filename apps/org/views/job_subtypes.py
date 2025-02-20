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
from ..constants import job_subtypes as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.JobSubtype.objects.all()
    serializer_class = serializers.JobSubtypeSerializer
    activity_serializer = serializers.JobSubtypeActivitySerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIJobSubtypeFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = Deleter

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return serializers.CreateUpdateJobSubtypeSerializer
        return super().get_serializer_class()


class ListView(
    PermissionRequiredMixin,
    mixins.BulkDeleteMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required = "org.view_jobsubtype"
    filter_class = filters.JobSubtypeFilter
    resource_class = resources.JobSubtypeResource
    activity_serializer = serializers.JobSubtypeActivitySerializer
    deleter = Deleter
    search_fields = constants.SEARCH_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("org.delete_jobsubtype",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "geo.view_jobsubtype"
    model = models.JobSubtype


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "org.add_jobsubtype"
    form_class = forms.JobSubtypeForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "org.change_jobsubtype"
    form_class = forms.JobSubtypeForm
    activity_serializer = serializers.JobSubtypeActivitySerializer


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "org.delete_jobsubtype"
    deleter = Deleter
    activity_serializer = serializers.JobSubtypeActivitySerializer
