from django.conf import settings
from django.db import models
from django.db.models.functions import Concat
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured

from apps.core.utils import (
    annotate_search,
    db_calculate_age_in_years,
    db_get_next_anniversary,
)

from ...constants import employee as constants


class AnnotationMixin:
    def _annotate_search(self, queryset: models.QuerySet):
        return queryset.annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )

    def _annotate_names(self, queryset: models.QuerySet):
        return queryset.annotate(
            fullname=Concat(
                models.F("firstname"),
                models.Value(" "),
                models.F("father_name"),
                models.Value(" "),
                models.F("lastname"),
            ),
            shortname=Concat(
                models.F("firstname"), models.Value(" "), models.F("lastname")
            ),
            father_fullname=Concat(
                models.F("father_name"), models.Value(" "), models.F("lastname")
            ),
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

        current_date = timezone.now()

        next_birthday = db_get_next_anniversary(
            field_name="birth_date",
            label="birthday",
            date=current_date,
        )
        next_job_anniversary = db_get_next_anniversary(
            field_name="hire_date",
            label="job_anniversary",
            n=settings.NTH_JOB_ANNIVERSARY or 2,
            date=current_date,
        )

        dates = {
            "age": db_calculate_age_in_years("birth_date", current_date),
            **next_birthday,
            "job_age": db_calculate_age_in_years("hire_date", current_date),
            **next_job_anniversary,
        }

        return queryset.annotate(**dates)
