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
from ..constants import departments as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    activity_serializer = serializers.DepartmentActivitySerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIDepartmentFilter
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
    permission_required = "org.view_department"
    filter_class = filters.DepartmentFilter
    resource_class = resources.DepartmentResource
    activity_serializer = serializers.DepartmentActivitySerializer
    deleter = Deleter
    search_fields = constants.SEARCH_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("org.delete_department",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "geo.view_department"
    model = models.Department


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "org.add_department"
    form_class = forms.DepartmentForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "org.change_department"
    form_class = forms.DepartmentForm
    activity_serializer = serializers.DepartmentActivitySerializer


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "org.delete_department"
    deleter = Deleter
    activity_serializer = serializers.DepartmentActivitySerializer
