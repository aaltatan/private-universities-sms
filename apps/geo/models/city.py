from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search
from apps.core.querysets import (
    EmployeesCountQuerysetMixin,
    EmployeesCountManagerMixin,
)

from ..constants import cities as constants
from .governorate import Governorate


class CityQuerySet(
    EmployeesCountQuerysetMixin["CityQuerySet"],
    models.QuerySet,
):
    pass


class CityManager(EmployeesCountManagerMixin[CityQuerySet], models.Manager):
    def get_queryset(self):
        queryset = CityQuerySet(self.model, using=self._db)
        return queryset.select_related("governorate").annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )


class City(AddCreateActivityMixin, AbstractUniqueNameModel):
    class KindChoices(models.TextChoices):
        CITY = "city", _("city").title()
        AREA = "area", _("area").title()
        TOWN = "town", _("town").title()
        VILLAGE = "village", _("village").title()
        OTHER = "other", _("other").title()

    governorate = models.ForeignKey(
        Governorate,
        on_delete=models.PROTECT,
        related_name="cities",
        verbose_name=_("governorate"),
    )
    kind = models.CharField(
        max_length=10,
        choices=KindChoices.choices,
        default=KindChoices.CITY,
        verbose_name=_("kind"),
    )

    objects: CityManager = CityManager()

    class Meta:
        icon = "home-modern"
        ordering = ("kind", "name")
        codename_plural = "cities"
        verbose_name = _("city").title()
        verbose_name_plural = _("cities").title()
        permissions = (
            ("export_city", "Can export city"),
            ("view_activity_city", "Can view city activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    governorate = serializers.CharField(source="governorate.name")

    class Meta:
        model = City
        fields = ("name", "governorate", "description")


pre_save.connect(signals.slugify_name, sender=City)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=City)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=City)
