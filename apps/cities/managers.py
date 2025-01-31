from django.db import models

from apps.core.utils import annotate_search

from .constants import SEARCH_FIELDS


class CityManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("governorate")
            .annotate(
                search=annotate_search(SEARCH_FIELDS),
            )
        )
