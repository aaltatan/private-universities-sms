from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import governorates as constants


class GovernorateQuerySet(models.QuerySet):
    def annotate_employees_count(self):
        return self.annotate(
            employees_count=models.Count("cities__employees", distinct=True),
        )

    def annotate_cities_count(self):
        return self.annotate(
            cities_count=models.Count("cities", distinct=True),
        )


class GovernorateManager(models.Manager):
    def annotate_employees_count(self):
        return self.get_queryset().annotate_employees_count()

    def annotate_cities_count(self):
        return self.get_queryset().annotate_cities_count()

    def get_queryset(self):
        queryset = GovernorateQuerySet(self.model, using=self._db)
        return queryset.prefetch_related("cities").annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )


class Governorate(AddCreateActivityMixin, AbstractUniqueNameModel):
    objects: GovernorateManager = GovernorateManager()

    class Meta:
        icon = "home-modern"
        ordering = ("name",)
        codename_plural = "governorates"
        verbose_name = _("governorate")
        verbose_name_plural = _("governorates")
        permissions = (
            ("export_governorate", "Can export governorate"),
            ("view_activity_governorate", "Can view governorate activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Governorate
        fields = ("name", "description")


pre_save.connect(signals.slugify_name, sender=Governorate)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Governorate)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Governorate)
