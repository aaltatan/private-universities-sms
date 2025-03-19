from django.db import models
from django.db.models import ExpressionWrapper, F, Value
from django.db.models.functions import Concat, Floor
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
            shortname=Concat(
                F("firstname"),
                Value(" "),
                F("lastname"),
            ),
        )

    def _annotate_ages(self, queryset: models.QuerySet):
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
        )
