from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import DetailView, View
from django.views.generic.list import MultipleObjectMixin
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets
from rest_framework.serializers import ValidationError

from apps.core import filter_backends, mixins
from apps.core.schemas import Action

from .. import filters, forms, models, resources, serializers, utils
from ..constants import exchange_rates as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.ExchangeRate.objects.all()
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIExchangeRateFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = utils.ExchangeRateDeleter

    def perform_create(self, serializer):
        if serializer.validated_data["currency"].is_primary:
            raise ValidationError(
                _("can't create primary currency"),
                code="invalid",
            )
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        instance = models.ExchangeRate.objects.get(pk=serializer.instance.pk)
        if instance.currency.is_primary:
            raise ValidationError(
                _("can't update primary currency"),
                code="invalid",
            )
        return super().perform_update(serializer)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return serializers.ExchangeRateCreateUpdateSerializer
        return serializers.ExchangeRateSerializer


class ListView(
    PermissionRequiredMixin,
    mixins.BulkDeleteMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required = "fin.view_exchangerate"
    model = models.ExchangeRate
    filter_class = filters.ExchangeRateFilter
    resource_class = resources.ExchangeRateResource
    deleter = utils.ExchangeRateDeleter
    ordering_fields = constants.ORDERING_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("fin.delete_exchangerate",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "fin.view_exchangerate"
    model = models.ExchangeRate


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "fin.add_exchangerate"
    form_class = forms.ExchangeRateForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "fin.change_exchangerate"
    form_class = forms.ExchangeRateForm

    def perform_update_before_validation(self, obj, form):
        if obj.currency.is_primary:
            form.add_error(None, _("can't update primary currency"))


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "fin.delete_exchangerate"
    deleter = utils.ExchangeRateDeleter
    model = models.ExchangeRate
