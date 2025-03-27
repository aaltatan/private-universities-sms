from django.db import models
from django.db.models import DateField, ExpressionWrapper, F, Func, Value
from django.db.models.functions import Concat, ExtractDay, ExtractMonth, Floor
from django.utils import timezone

from apps.core.utils import annotate_search

from ...constants import employee as constants


class AnnotationMixin:
    def _annotate_search(self, queryset: models.QuerySet):
        return queryset.annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )

    def _annotate_names(self, queryset: models.QuerySet):
        return queryset.annotate(
            fullname=Concat(
                F("firstname"),
                Value(" "),
                F("father_name"),
                Value(" "),
                F("lastname"),
            ),
            shortname=Concat(F("firstname"), Value(" "), F("lastname")),
            father_fullname=Concat(F("father_name"), Value(" "), F("lastname")),
        )

    def _annotate_dates(self, queryset: models.QuerySet):
        current_year = timezone.datetime.now().year

        return queryset.annotate(
            age=ExpressionWrapper(
                Floor(
                    (timezone.now().date() - F("birth_date"))
                    / timezone.timedelta(days=365)
                ),
                output_field=models.IntegerField(),
            ),
            job_age=ExpressionWrapper(
                Floor(
                    (timezone.now().date() - F("hire_date"))
                    / timezone.timedelta(days=365)
                ),
                output_field=models.IntegerField(),
            ),
            birth_month=ExtractMonth("birth_date"),
            birth_day=ExtractDay("birth_date"),
            next_birthday=Func(
                Value(current_year),
                Func(F("birth_date"), function="DAYOFYEAR"),
                function="MAKEDATE",
                output_field=DateField(),
            ),
        )
