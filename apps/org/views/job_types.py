from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.inline import InlineFormsetFactory
from apps.core.schemas import Action
from apps.core.utils import Deleter

from .. import filters, forms, models, resources, serializers
from ..constants import job_types as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = (
        models.JobType.objects.annotate_employees_count()
        .annotate_job_subtypes_count()
        .all()
    )
    serializer_class = serializers.JobTypeSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIJobTypeFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = Deleter


class ListView(PermissionRequiredMixin, mixins.ListMixin, View):
    permission_required = "org.view_jobtype"
    model = models.JobType
    filter_class = filters.JobTypeFilter
    resource_class = resources.JobTypeResource
    ordering_fields = constants.ORDERING_FIELDS

    def get_queryset(self):
        return (
            models.JobType.objects.annotate_employees_count()
            .annotate_job_subtypes_count()
            .all()
        )

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                behavior=Deleter,
                template="components/blocks/modals/bulk-delete.html",
                permissions=("org.delete_jobtype",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "org.view_jobtype"
    model = models.JobType

    def get_queryset(self):
        return (
            models.JobType.objects.annotate_employees_count()
            .annotate_job_subtypes_count()
            .all()
        )


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "org.add_jobtype"
    form_class = forms.JobTypeForm


class JobSubtypeInline(InlineFormsetFactory):
    model = models.JobSubtype
    form_class = forms.JobSubtypeForm
    fields = ("name", "description")
    deleter = Deleter

    @classmethod
    def get_queryset(cls, obj: models.JobType):
        return obj.job_subtypes.all().order_by("ordering", "id")


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "org.change_jobtype"
    form_class = forms.JobTypeForm
    inlines = (JobSubtypeInline,)


class DeleteView(PermissionRequiredMixin, mixins.BehaviorMixin, View):
    permission_required = "org.delete_jobtype"
    behavior = Deleter
    model = models.JobType
