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

from ..constants import specialization as constants


class SpecializationQuerySet(
    EmployeesCountQuerysetMixin["SpecializationQuerySet"],
    models.QuerySet,
):
    pass


class SpecializationManager(
    EmployeesCountManagerMixin[SpecializationQuerySet], models.Manager
):
    def get_queryset(self):
        queryset = SpecializationQuerySet(self.model, using=self._db)
        return queryset.annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )


class Specialization(AddCreateActivityMixin, AbstractUniqueNameModel):
    class SpecialistChoices(models.TextChoices):
        SPECIALIST = True, _("specialist")
        SUPPORTER = False, _("supporter")

    is_specialist = models.BooleanField(
        verbose_name=_("is specialist"),
        default=True,
    )

    objects: SpecializationManager = SpecializationManager()

    class Meta:
        icon = "rectangle-group"
        codename_plural = "specializations"
        verbose_name = _("specialization")
        verbose_name_plural = _("specializations")
        ordering = ("-is_specialist", "name")
        permissions = (
            ("export_specialization", "Can export specialization"),
            ("view_activity_specialization", "Can view specialization activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ("name", "is_specialist", "description")


pre_save.connect(signals.slugify_name, sender=Specialization)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Specialization)
pre_delete.connect(
    signals.add_delete_activity(ActivitySerializer), sender=Specialization
)
