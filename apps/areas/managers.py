from django.db import models

from apps.core.utils import annotate_search

from .constants import cities, governorates


class GovernorateManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(governorates.SEARCH_FIELDS),
            )
        )


class CityManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("governorate")
            .annotate(
                search=annotate_search(cities.SEARCH_FIELDS),
            )
        )
