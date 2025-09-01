from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.querysets import (
    EmployeesCountManagerMixin,
    EmployeesCountQuerysetMixin,
)
from apps.core.utils import annotate_search

from ..constants import nationalities as constants


class NationalityQuerySet(
    EmployeesCountQuerysetMixin["NationalityQuerySet"],
    models.QuerySet,
):
    pass


class NationalityManager(
    EmployeesCountManagerMixin[NationalityQuerySet], models.Manager
):
    def get_queryset(self):
        queryset = NationalityQuerySet(self.model, using=self._db)
        return queryset.prefetch_related("schools").annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )


class Nationality(AddCreateActivityMixin, AbstractUniqueNameModel):
    class LocalityChoices(models.TextChoices):
        LOCAL = True, _("local")
        FOREIGN = False, _("foreign")

    is_local = models.BooleanField(
        verbose_name=_("is local"),
        default=False,
    )

    objects: NationalityManager = NationalityManager()

    def save(self, *args, **kwargs):
        Model = self.__class__
        objs = []

        if self.is_local:
            qs = Model.objects.exclude(pk=self.pk)
            for obj in qs:
                obj.is_local = False
                objs.append(obj)

            Model.objects.bulk_update(objs, ["is_local"])

        return super().save(*args, **kwargs)

    class Meta:
        icon = "globe-europe-africa"
        ordering = ("name",)
        codename_plural = "nationalities"
        verbose_name = _("nationality")
        verbose_name_plural = _("nationalities")
        permissions = (
            ("export_nationality", "Can export nationality"),
            ("view_activity_nationality", "Can view nationality activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = ("name", "is_local", "description")


pre_save.connect(signals.slugify_name, sender=Nationality)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Nationality)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Nationality)
