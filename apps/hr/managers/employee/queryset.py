from django.db.models import Count, QuerySet
from django.utils import timezone

from apps.core.constants import DATE_UNITS


class EmployeeQuerySet(QuerySet):
    """
    Custom QuerySet for Employee model.
    """

    def get_counts_grouped_by(self, group_by: str = "gender"):
        return self.values(group_by).annotate(counts=Count("pk"))

    def get_upcoming_birthdays(
        self, *, this: DATE_UNITS = "day", date: timezone.datetime | None = None
    ):
        """
        Returns a queryset of employees whose birthday is in the future."
        If date is not provided, the current date is used.

        Args:
            date (timezone.datetime | None): The date to check for upcoming birthdays.
            this (Literal["year", "month", "day"]): The unit to check for upcoming birthdays.
                Defaults to "day".
        """
        if date is None:
            date = timezone.datetime.now()

        filter_kwargs = {
            "year": {
                "next_birthday__gte": date,
                "next_birthday__year": date.year,
            },
            "month": {
                "birth_date__month": date.month,
                "birth_date__day__gte": date.day,
            },
            "day": {
                "birth_date__month": date.month,
                "birth_date__day": date.day,
            },
        }

        return self.filter(**filter_kwargs[this])

    def get_upcoming_job_anniversaries(
        self, *, this: DATE_UNITS = "day", date: timezone.datetime | None = None
    ):
        """
        Returns a queryset of employees whose birthday is in the future."
        If date is not provided, the current date is used.

        Args:
            date (timezone.datetime | None): The date to check for upcoming job anniversary.
            this (Literal["year", "month", "day"]): The unit to check for upcoming job anniversaries.
                Defaults to "day".
        """
        if date is None:
            date = timezone.datetime.now()

        filter_kwargs = {
            "year": {
                "next_nth_job_anniversary__gte": date,
                "next_nth_job_anniversary__year": date.year,
            },
            "month": {
                "hire_date__month": date.month,
                "hire_date__day__gte": date.day,
            },
            "day": {
                "hire_date__month": date.month,
                "hire_date__day": date.day,
            },
        }

        return self.filter(**filter_kwargs[this])
