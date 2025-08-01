from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.schemas import Action
from apps.core.utils import Deleter

from .. import filters, forms, models, resources, serializers
from ..constants import voucher_kinds as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.VoucherKind.objects.annotate_vouchers_count().all()
    serializer_class = serializers.VoucherKindSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIVoucherKindFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = Deleter


class ListView(PermissionRequiredMixin, mixins.ListMixin, View):
    permission_required = "fin.view_voucherkind"
    model = models.VoucherKind
    filter_class = filters.VoucherKindFilter
    resource_class = resources.VoucherKindResource
    ordering_fields = constants.ORDERING_FIELDS

    def get_queryset(self):
        return models.VoucherKind.objects.annotate_vouchers_count().all()

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                behavior=Deleter,
                template="components/blocks/modals/bulk-delete.html",
                permissions=("fin.delete_voucherkind",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "fin.view_voucherkind"
    model = models.VoucherKind

    def get_queryset(self):
        return models.VoucherKind.objects.annotate_vouchers_count().all()


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "fin.add_voucherkind"
    form_class = forms.VoucherKindForm


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "fin.change_voucherkind"
    form_class = forms.VoucherKindForm


class DeleteView(PermissionRequiredMixin, mixins.BehaviorMixin, View):
    permission_required = "fin.delete_voucherkind"
    behavior = Deleter
    model = models.VoucherKind
