from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
from django.views.generic.list import MultipleObjectMixin
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.schemas import Action
from apps.core.utils import Deleter
from apps.core.inline import InlineFormsetFactory

from .. import filters, forms, models, resources, serializers
from ..constants import governorates as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Governorate.objects.all()
    serializer_class = serializers.GovernorateSerializer
    activity_serializer = serializers.GovernorateActivitySerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIGovernoratesFilter
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
    permission_required = "geo.view_governorate"
    filter_class = filters.GovernorateFilter
    resource_class = resources.GovernorateResource
    activity_serializer = serializers.GovernorateActivitySerializer
    deleter = Deleter
    search_fields = constants.SEARCH_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("geo.delete_governorate",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "geo.view_governorate"
    model = models.Governorate


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "geo.add_governorate"
    form_class = forms.GovernorateForm


class CityInline(InlineFormsetFactory):
    model = models.City
    form_class = forms.CityForm
    fields = ("name", "description")
    can_delete_permission = "geo.delete_city"
    extra = 1


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "geo.change_governorate"
    form_class = forms.GovernorateForm
    activity_serializer = serializers.GovernorateActivitySerializer
    inlines = {
        "cities": CityInline,
    }


class CitiesFormsetView(PermissionRequiredMixin, mixins.FormsetMixin, View):
    parent_model = models.Governorate
    model = models.City
    form_class = forms.CityForm
    fields = ("name", "description")
    can_delete_permission = "geo.delete_city"
    verbose_name_plural = "cities"
    permission_required = "geo.change_city"
    extra = 200

    def get_queryset(self):
        return self.obj.cities.all().order_by("id")


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "geo.delete_governorate"
    deleter = Deleter
    activity_serializer = serializers.GovernorateActivitySerializer
