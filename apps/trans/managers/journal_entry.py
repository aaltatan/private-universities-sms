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
        )
