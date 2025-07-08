from django.db import models, transaction

from apps.core.utils import annotate_search

from ..constants import journal_entries as constants


class JournalEntryManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "voucher",
                "employee",
                "cost_center",
                "period",
                "period__year",
                "content_type",
            )
            .prefetch_related("fiscal_object")
        ).annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
            net=models.Window(
                expression=models.Sum(models.F("amount")),
                frame=models.RowRange(None, 0),
                order_by=self.model._meta.ordering,
                output_field=models.DecimalField(
                    max_digits=20,
                    decimal_places=4,
                ),
            ),
        )

    def get_next_journal_general_serial(self) -> str:
        with transaction.atomic():
            last = self.select_for_update().order_by("-general_serial").first()
            return last.general_serial + 1 if last else 1
