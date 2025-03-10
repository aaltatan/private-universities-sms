from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import job_subtypes as constants
from .job_type import JobType


class JobSubtypeManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("job_type")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class JobSubtype(AbstractUniqueNameModel):
    job_type = models.ForeignKey(
        JobType,
        on_delete=models.PROTECT,
        related_name="job_subtypes",
    )

    objects: JobSubtypeManager = JobSubtypeManager()

    class Meta:
        icon = "briefcase"
        codename_plural = "job_subtypes"
        verbose_name = _("job subtype").title()
        verbose_name_plural = _("job subtypes").title()
        ordering = (
            "job_type__name",
            "name",
        )
        permissions = (
            ("export_jobsubtype", "Can export job_subtype"),
            ("view_activity_jobsubtype", "Can view job_subtype activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    job_type = serializers.CharField(source="job_type.name")

    class Meta:
        model = JobSubtype
        fields = ("name", "job_type", "description")


pre_save.connect(signals.slugify_name, sender=JobSubtype)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=JobSubtype)
