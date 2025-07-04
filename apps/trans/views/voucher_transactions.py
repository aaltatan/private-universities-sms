from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View
from django.views.generic.list import MultipleObjectMixin

from apps.core import mixins

from .. import filters, models, resources
from ..constants import voucher_transactions as constants
from ..utils import VoucherDeleter


class ListView(
    PermissionRequiredMixin,
    mixins.BulkDeleteMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required = "trans.view_vouchertransaction"
    model = models.VoucherTransaction
    filter_class = filters.VoucherTransactionFilter
    resource_class = resources.VoucherTransactionResource
    deleter = VoucherDeleter
    ordering_fields = constants.ORDERING_FIELDS
    queryset = models.VoucherTransaction.objects.filter(
        voucher__is_deleted=False,
    ).order_by("-voucher__voucher_serial", "voucher__date", "ordering")

    def get_actions(self):
        return {}
