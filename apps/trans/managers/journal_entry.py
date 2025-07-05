from django.db import models

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
                output_field=models.DecimalField(
                    max_digits=20,
                    decimal_places=4,
                ),
            ),
        )
