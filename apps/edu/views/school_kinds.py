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
from ..constants import school_kinds as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.SchoolKind.objects.all().order_by("name")
    serializer_class = serializers.SchoolKindSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APISchoolKindFilter
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
    permission_required = "edu.view_schoolkind"
    filter_class = filters.SchoolKindFilter
    resource_class = resources.SchoolKindResource
    deleter = Deleter
    search_fields = constants.SEARCH_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("edu.delete_schoolkind",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "edu.view_schoolkind"
    model = models.SchoolKind


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "edu.add_schoolkind"
    form_class = forms.SchoolKindForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "edu.change_schoolkind"
    form_class = forms.SchoolKindForm


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "edu.delete_schoolkind"
    deleter = Deleter
    model = models.SchoolKind
