from django.db import models
from django.db.models.signals import pre_save

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search

from ..constants import job_subtypes
from .job_type import JobType


class JobSubtypeManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("job_type")
            .annotate(
                search=annotate_search(job_subtypes.SEARCH_FIELDS),
            )
        )


class JobSubtype(AbstractUniqueNameModel):
    job_type = models.ForeignKey(
        JobType,
        on_delete=models.PROTECT,
        related_name="job_subtypes",
    )

    objects = JobSubtypeManager()

    class Meta:
        ordering = (
            "job_type__name",
            "name",
        )
        verbose_name_plural = "job_subtypes"
        permissions = (
            ("export_jobsubtype", "Can export job_subtype"),
            ("view_activity_jobsubtype", "Can view job_subtype activity"),
        )


pre_save.connect(slugify_name, sender=JobSubtype)
