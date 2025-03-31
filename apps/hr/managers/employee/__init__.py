from django.db import models
from django.utils import timezone

from .annotations import AnnotationMixin
from .optimizations import OptimizationMixin
from .queryset import EmployeeQuerySet

from apps.core.constants import DATE_UNITS

class EmployeeManager(AnnotationMixin, OptimizationMixin, models.Manager):
    def get_counts_grouped_by(self, group_by: str = "gender"):
        return (
            self.get_queryset()
            .values(group_by)
            .annotate(
                counts=models.Count("pk"),
            )
        )

    def get_upcoming_birthdays(
        self,
        *,
        this: DATE_UNITS = "day",
        date: timezone.datetime | None = None,
    ) -> EmployeeQuerySet:
        """
        Returns a queryset of employees whose birthday is in the future."
        If date is not provided, the current date is used.

        Args:
            date (timezone.datetime | None): The date to check for upcoming birthdays.
            this (Literal["year", "month", "day"]): The unit to check for upcoming birthdays.
                Defaults to "day".
        """
        return self.get_queryset().get_upcoming_birthdays(date=date, this=this)

    def get_upcoming_job_anniversaries(
        self,
        *,
        this: DATE_UNITS = "day",
        date: timezone.datetime | None = None,
    ) -> EmployeeQuerySet:
        """
        Returns a queryset of employees whose birthday is in the future."
        If date is not provided, the current date is used.

        Args:
            date (timezone.datetime | None): The date to check for upcoming job anniversary.
            this (Literal["year", "month", "day"]): The unit to check for upcoming job anniversaries.
                Defaults to "day".
        """
        return self.get_queryset().get_upcoming_job_anniversaries(date=date, this=this)

    def get_queryset(self) -> EmployeeQuerySet:
        queryset = EmployeeQuerySet(self.model, using=self._db)

        # optimizations
        queryset = self._select_related(queryset)
        queryset = self._prefetch_related(queryset)

        # annotations
        queryset = self._annotate_search(queryset)
        queryset = self._annotate_names(queryset)
        queryset = self._annotate_dates(queryset)

        return queryset
