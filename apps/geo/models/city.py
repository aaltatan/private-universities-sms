from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search

from ..constants import cities as constants
from .governorate import Governorate


class CityManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("governorate")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class City(AbstractUniqueNameModel):
    governorate = models.ForeignKey(
        Governorate,
        on_delete=models.PROTECT,
        related_name="cities",
    )

    objects: CityManager = CityManager()

    class Meta:
        icon = "home-modern"
        title = _("cities")
        ordering = ("name",)
        verbose_name_plural = "cities"
        permissions = (
            ("export_city", "Can export city"),
            ("view_activity_city", "Can view city activity"),
        )


pre_save.connect(slugify_name, sender=City)
