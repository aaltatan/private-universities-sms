from typing import Literal

from django.db import models
from django.db.models.functions import ExtractDay, ExtractMonth
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

        qs = self.annotate(
            birth_day=ExtractDay("birth_date"),
            birth_month=ExtractMonth("birth_date"),
        )

        filter_kwargs = {
            "year": {
                "birth_month__gte": date.month,
            },
            "month": {
                "birth_month": date.month,
                "birth_day__gte": date.day,
            },
            "day": {
                "birth_month": date.month,
                "birth_day": date.day,
            }
        }

        return qs.filter(**filter_kwargs[this])
