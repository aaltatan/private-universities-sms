from django.db import models
from django.utils import timezone

from apps.core.constants import DATE_UNITS
from apps.core.querysets import JournalsTotalsManagerMixin

from ..constants.employee import PREFETCH_RELATED_LOOKUPS, SELECT_RELATED_FIELDS
from ..querysets import EmployeeQuerySet


class EmployeeManager(JournalsTotalsManagerMixin[EmployeeQuerySet], models.Manager):
    def annotate_search(self):
        return self.get_queryset().annotate_search()

    def annotate_dates(
        self,
        nth_job_anniversary: int = 2,
        years_count_to_group_job_age: int = 2,
    ):
        return self.get_queryset().annotate_dates(
            nth_job_anniversary=nth_job_anniversary,
            years_count_to_group_job_age=years_count_to_group_job_age,
        )

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

    def select_related(self, *fields: SELECT_RELATED_FIELDS):
        return super().select_related(*fields)

    def prefetch_related(self, *lookups: PREFETCH_RELATED_LOOKUPS):
        return super().prefetch_related(*lookups)

    def get_queryset(self) -> EmployeeQuerySet:
        queryset = EmployeeQuerySet(self.model, using=self._db)
        queryset = queryset.annotate_search().select_related("cost_center")

        return queryset
