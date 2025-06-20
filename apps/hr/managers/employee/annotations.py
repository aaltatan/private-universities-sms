from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.functions import Floor
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.utils import (
    annotate_search,
    db_calculate_age_in_years,
    db_get_age_groups,
    db_get_next_anniversary,
)

from ...constants import employee as constants


class AnnotationMixin:
    def _annotate_search(self, queryset: models.QuerySet):
        return queryset.annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )

    def _annotate_dates(self, queryset: models.QuerySet):
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
            "age": db_calculate_age_in_years("birth_date", current_date),
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
            "job_age": db_calculate_age_in_years("hire_date", current_date),
            "job_age_group": db_get_age_groups(
                "job_age", n=settings.YEARS_COUNT_TO_GROUP_JOB_AGE
            ),
            **next_job_anniversary,
        }

        return queryset.annotate(**dates)
