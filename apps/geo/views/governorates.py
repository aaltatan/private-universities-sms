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
from ..constants import governorates as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = (
        models.Governorate.objects.annotate_cities_count()
        .annotate_employees_count()
        .all()
    )
    serializer_class = serializers.GovernorateSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIGovernorateFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = Deleter


class ListView(PermissionRequiredMixin, mixins.ListMixin, View):
    permission_required = "geo.view_governorate"
    model = models.Governorate
    filter_class = filters.GovernorateFilter
    resource_class = resources.GovernorateResource
    ordering_fields = constants.ORDERING_FIELDS

    def get_queryset(self):
        return (
            models.Governorate.objects.annotate_cities_count()
            .annotate_employees_count()
            .all()
        )

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                behavior=Deleter,
                template="components/blocks/modals/bulk-delete.html",
                permissions=("geo.delete_governorate",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "geo.view_governorate"
    model = models.Governorate

    def get_queryset(self):
        return (
            models.Governorate.objects.annotate_cities_count()
            .annotate_employees_count()
            .all()
        )


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "geo.add_governorate"
    form_class = forms.GovernorateForm


class CityInline(InlineFormsetFactory):
    model = models.City
    form_class = forms.CityForm
    fields = ("name", "kind", "description")
    deleter = Deleter

    @classmethod
    def get_queryset(cls, obj: models.Governorate):
        return obj.cities.all().order_by("ordering", "id")


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "geo.change_governorate"
    form_class = forms.GovernorateForm
    inlines = (CityInline,)


class DeleteView(PermissionRequiredMixin, mixins.BehaviorMixin, View):
    permission_required = "geo.delete_governorate"
    behavior = Deleter
    model = models.Governorate
