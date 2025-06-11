import re

from django.db import models, transaction

from apps.core.utils import annotate_search

from ..constants import vouchers as constants


class BaseVoucherManager(models.Manager):
    select_related_list = (
        "kind",
        "period",
        "created_by",
        "updated_by",
        "audited_by",
    )
    prefetch_related_list = ("transactions",)
    annotations = {
        "search": annotate_search(constants.SEARCH_FIELDS),
        "transactions_count": models.Count("transactions"),
        "total": models.Sum(
            models.F("transactions__quantity") * models.F("transactions__value")
        ),
        "net": models.Sum(
            (models.F("transactions__quantity") * models.F("transactions__value"))
            - models.F("transactions__tax")
        ),
    }

    def get_next_voucher_serial(self) -> str:
        with transaction.atomic():
            last = self.select_for_update().order_by("-voucher_serial").first()
            if last:
                serial = re.search(r"\d+$", last.voucher_serial)
                next_serial = int(serial.group()) + 1 if serial else 1
            else:
                next_serial = 1
            return f"VOC{next_serial:012d}"


class VoucherManager(BaseVoucherManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(*self.prefetch_related_list)
            .select_related(*self.select_related_list)
            .filter(is_deleted=False)
            .annotate(**self.annotations)
        )


class VoucherProxyManager(BaseVoucherManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(*self.prefetch_related_list)
            .select_related(*self.select_related_list)
            .annotate(**self.annotations)
        )
