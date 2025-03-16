from django.db import models


class OptimizationMixin:
    def _select_related(self, queryset: models.QuerySet):
        return queryset.select_related(
            # geo
            "city",
            "nationality",
            # org
            "cost_center",
            "position",
            "status",
            "job_subtype",
            # edu
            "degree",
            "school",
            "specialization",
        )

    def _prefetch_related(self, queryset: models.QuerySet):
        return queryset.prefetch_related("groups")
