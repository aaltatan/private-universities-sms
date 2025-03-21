from django.db import models
from django.utils import timezone

from .annotations import AnnotationMixin
from .optimizations import OptimizationMixin
from .queryset import EmployeeQuerySet


class EmployeeManager(AnnotationMixin, OptimizationMixin, models.Manager):
    def get_upcoming_birthdays(
        self, date: timezone.datetime | None = None, today: bool = True
    ) -> EmployeeQuerySet:
        return self.get_queryset().get_upcoming_birthdays(date, today)

    def get_queryset(self) -> EmployeeQuerySet:
        queryset = EmployeeQuerySet(self.model, using=self._db)

        # optimizations
        queryset = self._select_related(queryset)
        queryset = self._prefetch_related(queryset)

        # annotations
        queryset = self._annotate_search(queryset)
        queryset = self._annotate_names(queryset)
        queryset = self._annotate_ages(queryset)

        return queryset
