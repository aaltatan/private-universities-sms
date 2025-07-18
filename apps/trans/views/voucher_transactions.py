from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View

from apps.core import mixins

from .. import filters, models, resources
from ..constants import voucher_transactions as constants


class ListView(PermissionRequiredMixin, mixins.ListMixin, View):
    permission_required = "trans.view_vouchertransaction"
    model = models.VoucherTransaction
    filter_class = filters.VoucherTransactionFilter
    resource_class = resources.VoucherTransactionResource
    ordering_fields = constants.ORDERING_FIELDS

    def get_queryset(self):
        return models.VoucherTransaction.objects.filter(
            voucher__is_deleted=False,
        )

    def get_actions(self):
        return {}
