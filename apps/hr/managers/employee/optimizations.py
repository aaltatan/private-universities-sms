from django.db import models

from ...constants.employee import (
    PREFETCH_RELATED_FIELDS,
    SELECT_RELATED_FIELDS,
)


class OptimizationMixin:
    def _select_related(
        self, queryset: models.QuerySet, fields: list[SELECT_RELATED_FIELDS]
    ):
        return queryset.select_related(*fields)

    def _prefetch_related(
        self, queryset: models.QuerySet, fields: list[PREFETCH_RELATED_FIELDS]
    ):
        return queryset.prefetch_related(*fields)
