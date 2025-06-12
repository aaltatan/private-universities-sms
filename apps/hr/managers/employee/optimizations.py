from django.db import models


class OptimizationMixin:
    def _select_related(self, queryset: models.QuerySet):
        return queryset.select_related(
            # geo
            "city",
            "city__governorate",
            "nationality",
            # org
            "cost_center",
            "position",
            "status",
            "job_subtype",
            "job_subtype__job_type",
            # edu
            "degree",
            "school",
            "school__kind",
            "specialization",
        )

    def _prefetch_related(self, queryset: models.QuerySet):
        return queryset.prefetch_related(
            "groups",
            "emails",
            "phones",
            "mobiles",
        )
