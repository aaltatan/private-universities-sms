from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import specialization as constants


class SpecializationManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Specialization(AbstractUniqueNameModel):
    class SpecialistChoices(models.TextChoices):
        SPECIALIST = True, _("specialist").title()
        SUPPORTER = False, _("supporter").title()

    is_specialist = models.BooleanField(
        verbose_name=_("is specialist"),
        default=True,
        help_text=_("is a specialist or supporter"),
    )

    objects: SpecializationManager = SpecializationManager()

    class Meta:
        icon = "rectangle-group"
        codename_plural = "specializations"
        verbose_name = _("specialization").title()
        verbose_name_plural = _("specializations").title()
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
