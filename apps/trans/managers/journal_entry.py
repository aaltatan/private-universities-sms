from django.db import models


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
                "content_type",
            )
            .prefetch_related("fiscal_object")
        ).annotate(
            net=models.Window(
                expression=models.Sum(models.F("amount")),
                frame=models.RowRange(0, None),
                order_by=("-date", "ordering", "-debit"),
                output_field=models.DecimalField(
                    max_digits=20,
                    decimal_places=4,
                ),
            )
        )
