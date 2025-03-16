from django.db import models

from .annotations import AnnotationMixin
from .optimizations import OptimizationMixin


class EmployeeManager(
    AnnotationMixin,
    OptimizationMixin,
    models.Manager,
):
    def get_queryset(self):
        queryset = super().get_queryset()

        # optimizations
        queryset = self._select_related(queryset)
        queryset = self._prefetch_related(queryset)

        # annotations
        queryset = self._annotate_search(queryset)
        queryset = self._annotate_names(queryset)
        queryset = self._annotate_ages(queryset)

        return queryset
