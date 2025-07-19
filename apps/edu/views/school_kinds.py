from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
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
    queryset = (
        models.SchoolKind.objects.annotate_employees_count()
        .annotate_schools_count()
        .all()
    )
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


class ListView(PermissionRequiredMixin, mixins.ListMixin, View):
    permission_required = "edu.view_schoolkind"
    model = models.SchoolKind
    filter_class = filters.SchoolKindFilter
    resource_class = resources.SchoolKindResource
    ordering_fields = constants.ORDERING_FIELDS

    def get_queryset(self):
        return (
            models.SchoolKind.objects.annotate_employees_count()
            .annotate_schools_count()
            .all()
        )

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                behavior=Deleter,
                template="components/blocks/modals/bulk-delete.html",
                permissions=("edu.delete_schoolkind",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "edu.view_schoolkind"
    model = models.SchoolKind

    def get_queryset(self):
        return (
            models.SchoolKind.objects.annotate_employees_count()
            .annotate_schools_count()
            .all()
        )


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "edu.add_schoolkind"
    form_class = forms.SchoolKindForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "edu.change_schoolkind"
    form_class = forms.SchoolKindForm


class DeleteView(PermissionRequiredMixin, mixins.BehaviorMixin, View):
    permission_required = "edu.delete_schoolkind"
    behavior = Deleter
    model = models.SchoolKind
