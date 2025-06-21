from decimal import Decimal

from django.db import models
from django.db.models.functions import Coalesce

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
            )
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
                total=Coalesce(models.F("quantity") * models.F("value"), Decimal(0)),
                net=Coalesce(models.F("total") - models.F("tax"), Decimal(0)),
            )
        )
