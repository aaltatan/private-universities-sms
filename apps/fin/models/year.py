from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import years as constants


class YearManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("periods")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Year(AddCreateActivityMixin, AbstractUniqueNameModel):
    objects: YearManager = YearManager()

    class Meta:
        icon = "calendar"
        ordering = ("name",)
        codename_plural = "years"
        verbose_name = _("year")
        verbose_name_plural = _("years")
        permissions = (
            ("export_year", "Can export year"),
            ("view_activity_year", "Can view year activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ("name", "description")


pre_save.connect(signals.slugify_name, sender=Year)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Year)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Year)
