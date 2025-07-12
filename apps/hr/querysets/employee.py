from typing import Literal

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.functions import Coalesce, Floor
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.constants import DATE_UNITS
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


class EmployeeQuerySet(models.QuerySet):
    """
    Custom QuerySet for Employee model.
    """

    def annotate_unmigrated_vouchers_totals(self, include_zero: bool = True):
        """
        Returns a queryset of employees with totals from their unmigrated vouchers.
        """
        queryset = self.annotate(
            unmigrated_total=Coalesce(
                models.Sum(
                    models.F("transactions__quantity")
                    * models.F("transactions__value"),
                    filter=models.Q(transactions__voucher__is_migrated=False),
                ),
                0,
                output_field=models.DecimalField(max_digits=20, decimal_places=4),
            )
        )

        if not include_zero:
            queryset = queryset.filter(~models.Q(unmigrated_total=0))

        return queryset

    def annotate_unmigrated_vouchers_nets(self, include_zero: bool = True):
        """
        Returns a queryset of employees with nets from their unmigrated vouchers.
        """
        queryset = self.annotate(
            unmigrated_net=Coalesce(
                models.Sum(
                    (
                        models.F("transactions__quantity")
                        * models.F("transactions__value")
                    )
                    - models.F("transactions__tax"),
                    filter=models.Q(transactions__voucher__is_migrated=False),
                ),
                0,
                output_field=models.DecimalField(max_digits=20, decimal_places=4),
            )
        )

        if not include_zero:
            queryset = queryset.filter(~models.Q(unmigrated_net=0))

        return queryset

    def _annotate_journals_total_field(
        self,
        field_name: Literal["debit", "credit", "amount"],
    ):
        """
        Returns a queryset of employees with totals from their journals.
        """
        return self.annotate(
            **{
                f"total_{field_name}": Coalesce(
                    models.Sum(f"journals__{field_name}"),
                    0,
                    output_field=models.DecimalField(
                        max_digits=20,
                        decimal_places=4,
                    ),
                )
            },
        )

    def annotate_journals_total_debit(self):
        return self._annotate_journals_total_field("debit")

    def annotate_journals_total_credit(self):
        return self._annotate_journals_total_field("credit")

    def annotate_journals_total_amount(self):
        return self._annotate_journals_total_field("amount")

    def annotate_search(self):
        return self.annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )

    def annotate_dates(self):
        if getattr(settings, "NTH_JOB_ANNIVERSARY", None) is None:
            raise ImproperlyConfigured("NTH_JOB_ANNIVERSARY is not set")

        if not isinstance(settings.NTH_JOB_ANNIVERSARY, int):
            raise ImproperlyConfigured("NTH_JOB_ANNIVERSARY must be an integer")

        if settings.NTH_JOB_ANNIVERSARY < 1:
            raise ImproperlyConfigured(
                "NTH_JOB_ANNIVERSARY must be greater than or equal to 1",
            )

        if getattr(settings, "YEARS_COUNT_TO_GROUP_JOB_AGE", None) is None:
            raise ImproperlyConfigured(
                "YEARS_COUNT_TO_GROUP_JOB_AGE is not set",
            )

        if not isinstance(settings.YEARS_COUNT_TO_GROUP_JOB_AGE, int):
            raise ImproperlyConfigured(
                "YEARS_COUNT_TO_GROUP_JOB_AGE must be an integer"
            )

        if settings.YEARS_COUNT_TO_GROUP_JOB_AGE < 2:
            raise ImproperlyConfigured(
                "YEARS_COUNT_TO_GROUP_JOB_AGE must be greater than or equal to 2",
            )

        current_date = timezone.now()

        next_birthday = db_get_next_anniversary(
            field_name="birth_date",
            label="birthday",
            date=current_date,
        )
        next_job_anniversary = db_get_next_anniversary(
            field_name="hire_date",
            label="job_anniversary",
            n=settings.NTH_JOB_ANNIVERSARY,
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
                "job_age", n=settings.YEARS_COUNT_TO_GROUP_JOB_AGE
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

        return (
            self.annotate_dates()
            .filter(**filter_kwargs[this])
            .order_by(
                "birth_date__day",
                "birth_date__year",
            )
        )

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

        return (
            self.annotate_dates()
            .filter(**filter_kwargs[this])
            .order_by("hire_date__day", "hire_date__year")
        )
