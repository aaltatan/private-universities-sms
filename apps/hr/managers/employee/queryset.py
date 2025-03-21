from django.db import models
from django.db.models.functions import ExtractDay, ExtractMonth
from django.utils import timezone


class EmployeeQuerySet(models.QuerySet):
    """
    Custom QuerySet for Employee model.
    """

    def get_upcoming_birthdays(
        self, date: timezone.datetime | None = None, today: bool = True
    ):
        if date is None:
            date = timezone.datetime.now()

        qs = self.annotate(
            birth_day=ExtractDay("birth_date"),
            birth_month=ExtractMonth("birth_date"),
        )

        if today:
            filter_kwargs = {"birth_day": date.day, "birth_month": date.month}
        else:
            filter_kwargs = {
                "birth_day__gte": date.day,
                "birth_month": date.month,
            }

        return qs.filter(**filter_kwargs)
