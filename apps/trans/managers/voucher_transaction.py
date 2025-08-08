from django.db import models

from apps.core.utils import annotate_search

from ..constants import voucher_transactions as constants


class VoucherTransactionManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "voucher",
                "employee",
                "employee__status",
                "employee__cost_center",
                "compensation",
                "compensation__tax",
            )
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )
