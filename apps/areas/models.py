from django.db import models
from django.db.models.signals import pre_save

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name

from .managers import CityManager, GovernorateManager


class Governorate(AbstractUniqueNameModel):
    objects = GovernorateManager()

    class Meta:
        ordering = ("name",)
        permissions = (("export_governorate", "Can export governorate"),)


class City(AbstractUniqueNameModel):
    governorate = models.ForeignKey(
        Governorate,
        on_delete=models.PROTECT,
        related_name="cities",
    )

    objects = CityManager()

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "cities"
        permissions = (("export_city", "Can export city"),)


pre_save.connect(slugify_name, sender=City)
pre_save.connect(slugify_name, sender=Governorate)
