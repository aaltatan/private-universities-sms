from django.db import models
from django.utils import timezone

from apps.core.constants import DATE_UNITS

from ...constants.employee import PREFETCH_RELATED_FIELDS, SELECT_RELATED_FIELDS
from .annotations import AnnotationMixin
from .optimizations import OptimizationMixin
from .queryset import EmployeeQuerySet


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

    def queryset_adjustments(
        self,
        *,
        select_related: list[SELECT_RELATED_FIELDS] | None = None,
        prefetch_related: list[PREFETCH_RELATED_FIELDS] | None = None,
        search_annotations: bool = True,
        date_annotations: bool = True,
    ):
        queryset = self.get_queryset()

        if select_related:
            queryset = self._select_related(queryset, select_related)

        if prefetch_related:
            queryset = self._prefetch_related(queryset, prefetch_related)

        if search_annotations:
            queryset = self._annotate_search(queryset)

        if date_annotations:
            queryset = self._annotate_dates(queryset)

        return queryset

    def get_queryset(self) -> EmployeeQuerySet:
        queryset = EmployeeQuerySet(self.model, using=self._db)
        queryset = self._annotate_search(queryset)
        return queryset
