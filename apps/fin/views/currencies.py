from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
from django.views.generic.list import MultipleObjectMixin
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.schemas import Action

from .. import filters, forms, models, resources, serializers, utils
from ..constants import currencies as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APICurrencyFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = utils.CurrencyDeleter


class ListView(
    PermissionRequiredMixin,
    mixins.BulkDeleteMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required = "org.view_currency"
    model = models.Currency
    filter_class = filters.CurrencyFilter
    resource_class = resources.CurrencyResource
    deleter = utils.CurrencyDeleter
    ordering_fields = constants.ORDERING_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("org.delete_currency",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "geo.view_currency"
    model = models.Currency


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "org.add_currency"
    form_class = forms.CurrencyForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "org.change_currency"
    form_class = forms.CurrencyForm


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "org.delete_currency"
    deleter = utils.CurrencyDeleter
    model = models.Currency
