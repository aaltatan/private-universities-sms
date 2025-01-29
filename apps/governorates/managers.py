from django.db import models

from apps.core.utils import annotate_search

from .constants import SEARCH_FIELDS


class GovernorateManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(SEARCH_FIELDS),
            )
        )
