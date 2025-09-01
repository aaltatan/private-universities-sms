from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import job_types as constants


class JobTypeQuerySet(models.QuerySet):
    def annotate_employees_count(self):
        return self.annotate(
            employees_count=models.Count("job_subtypes__employees", distinct=True),
        )

    def annotate_job_subtypes_count(self):
        return self.annotate(
            job_subtypes_count=models.Count("job_subtypes", distinct=True),
        )


class JobTypeManager(models.Manager):
    def annotate_employees_count(self):
        return self.get_queryset().annotate_employees_count()

    def annotate_job_subtypes_count(self):
        return self.get_queryset().annotate_job_subtypes_count()

    def get_queryset(self):
        queryset = JobTypeQuerySet(self.model, using=self._db)
        return queryset.prefetch_related("job_subtypes").annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )


class JobType(AddCreateActivityMixin, AbstractUniqueNameModel):
    objects: JobTypeManager = JobTypeManager()

    class Meta:
        icon = "briefcase"
        codename_plural = "job_types"
        verbose_name = _("job type")
        verbose_name_plural = _("job types")
        ordering = ("name",)
        permissions = (
            ("export_jobtype", "Can export job_type"),
            ("view_activity_jobtype", "Can view job_type activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ("name", "description")


pre_save.connect(signals.slugify_name, sender=JobType)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=JobType)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=JobType)
