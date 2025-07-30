from django.db import models
from django.db.models.functions import Floor
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.constants import DATE_UNITS
from apps.core.querysets import JournalsTotalsQuerysetMixin
from apps.core.utils import (
    annotate_search,
    db_calculate_age_in_years,
    db_get_age_groups,
    db_get_next_anniversary,
)

from ..constants import employee as constants
from ..constants.employee import (
    PREFETCH_RELATED_LOOKUPS,
    SELECT_RELATED_FIELDS,
)


class EmployeeQuerySet(
    JournalsTotalsQuerysetMixin["EmployeeQuerySet"], models.QuerySet
):
    """
    Custom QuerySet for Employee model.
    """

    def annotate_search(self):
        return self.annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )

    def annotate_dates(
        self,
        nth_job_anniversary: int,
        years_count_to_group_job_age: int,
    ):
        current_date = timezone.now()

        next_birthday = db_get_next_anniversary(
            field_name="birth_date",
            label="birthday",
            date=current_date,
        )
        next_job_anniversary = db_get_next_anniversary(
            field_name="hire_date",
            label="job_anniversary",
            n=nth_job_anniversary,
            date=current_date,
        )

        dates = {
            "age": db_calculate_age_in_years(
                "birth_date",
                other_date=current_date,
            ),
            "_age_group": Floor(models.F("age") / models.Value(10)),
            "age_group": models.Case(
                models.When(_age_group=0, then=_("children")),
                models.When(_age_group=1, then=_("10's")),
                models.When(_age_group=2, then=_("20's")),
                models.When(_age_group=3, then=_("30's")),
                models.When(_age_group=4, then=_("40's")),
                models.When(_age_group=5, then=_("50's")),
                models.When(_age_group=6, then=_("60's")),
                models.When(_age_group=7, then=_("70's")),
                models.When(_age_group=8, then=_("80's")),
                models.When(_age_group=9, then=_("90's")),
                default=_("above 100"),
                output_field=models.CharField(),
            ),
            **next_birthday,
            "job_age": models.Case(
                models.When(
                    separation_date__isnull=True,
                    then=db_calculate_age_in_years(
                        "hire_date", other_date=current_date
                    ),
                ),
                default=db_calculate_age_in_years(
                    "separation_date", other_fieldname="separation_date"
                ),
            ),
            "job_age_group": db_get_age_groups(
                "job_age", n=years_count_to_group_job_age
            ),
            **next_job_anniversary,
        }

        return self.annotate(**dates)

    def select_related(self, *fields: SELECT_RELATED_FIELDS):
        return super().select_related(*fields)

    def prefetch_related(self, *lookups: PREFETCH_RELATED_LOOKUPS):
        return super().prefetch_related(*lookups)

    def get_counts_grouped_by(self, group_by: str = "gender"):
        return self.values(group_by).annotate(counts=models.Count("pk"))

    def get_upcoming_birthdays(
        self,
        *,
        this: DATE_UNITS = "day",
        date: timezone.datetime | None = None,
        nth_job_anniversary: int = 2,
        years_count_to_group_job_age: int = 2,
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

        return (
            self.annotate_dates(
                nth_job_anniversary=nth_job_anniversary,
                years_count_to_group_job_age=years_count_to_group_job_age,
            )
            .filter(**filter_kwargs[this])
            .order_by(
                "birth_date__day",
                "birth_date__year",
            )
        )

    def get_upcoming_job_anniversaries(
        self,
        *,
        this: DATE_UNITS = "day",
        date: timezone.datetime | None = None,
        nth_job_anniversary: int = 2,
        years_count_to_group_job_age: int = 2,
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

        return (
            self.annotate_dates(
                nth_job_anniversary=nth_job_anniversary,
                years_count_to_group_job_age=years_count_to_group_job_age,
            )
            .filter(**filter_kwargs[this])
            .order_by("hire_date__day", "hire_date__year")
        )
