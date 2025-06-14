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
                "compensation",
            )
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
                total=models.F("quantity") * models.F("value"),
                net=models.F("total") - models.F("tax"),
            )
        )
