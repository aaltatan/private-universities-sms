from typing import Literal

from django.db import models
from django.utils import timezone


class EmployeeQuerySet(models.QuerySet):
    """
    Custom QuerySet for Employee model.
    """

    def get_upcoming_birthdays(
        self,
        *,
        this: Literal["year", "month", "day"] = "day",
        date: timezone.datetime | None = None,
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
            },
            "month": {
                "birth_month": date.month,
                "birth_day__gte": date.day,
            },
            "day": {
                "birth_month": date.month,
                "birth_day": date.day,
            },
        }

        return self.filter(**filter_kwargs[this])
