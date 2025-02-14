from django.db import models
from django.db.models.signals import pre_save

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search

from ..constants import job_types


class JobTypeManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(job_types.SEARCH_FIELDS),
            )
        )


class JobType(AbstractUniqueNameModel):
    objects = JobTypeManager()

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "job_types"
        permissions = (
            ("export_jobtype", "Can export job_type"),
            ("view_activity_jobtype", "Can view job_type activity"),
        )


pre_save.connect(slugify_name, sender=JobType)
