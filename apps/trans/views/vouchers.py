from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
from django.views.generic.list import MultipleObjectMixin
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
# from apps.core.inline import InlineFormsetFactory
from apps.core.schemas import Action
from apps.core.utils import Deleter

from .. import filters, forms, models, resources, serializers
from ..constants import vouchers as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Voucher.objects.all().order_by("voucher_serial")
    serializer_class = serializers.VoucherSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIVoucherFilter
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
    permission_required = "trans.view_voucher"
    model = models.Voucher
    filter_class = filters.VoucherFilter
    resource_class = resources.VoucherResource
    deleter = Deleter
    ordering_fields = constants.ORDERING_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("trans.delete_voucher",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "trans.view_voucher"
    model = models.Voucher


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "trans.add_voucher"
    form_class = forms.VoucherForm


# class VoucherTransactionInline(InlineFormsetFactory):
#     model = models.VoucherTransaction
#     form_class = forms.VoucherTransactionForm
#     fields = ("name", "kind", "description")

#     @classmethod
#     def get_queryset(cls, obj: models.Voucher):
#         return obj.transactions.all().order_by("ordering", "id")


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "trans.change_voucher"
    form_class = forms.VoucherForm
    # inlines = (VoucherTransactionInline,)


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "trans.delete_voucher"
    deleter = Deleter
    model = models.Voucher
