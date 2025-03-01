from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from apps.core.models import AbstractUniqueNameModel
from apps.core.schemas import ReportSchema
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search

from ..constants import job_types as constants


class JobTypeManager(models.Manager):
    def get_report_job_types_count(self, include_zeros=False) -> ReportSchema:
        """
        Returns a queryset of job subtypes with the number of job types in each.
        """
        report = (
            self.get_queryset()
            .values("name")
            .annotate(
                counts=models.Count("job_subtypes"),
            )
        )
        if not include_zeros:
            report = report.filter(counts__gt=0)

        report_schema = ReportSchema(
            title=_("job subtypes count"),
            headers=[_("name"), _("count")],
            report=list(report),
        )

        return report_schema

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("job_subtypes")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
                job_subtypes_count=models.Count("job_subtypes"),
            )
        )


class JobType(AbstractUniqueNameModel):
    objects: JobTypeManager = JobTypeManager()

    class Meta:
        icon = "briefcase"
        title = _("job types")
        ordering = ("name",)
        verbose_name_plural = "job_types"
        permissions = (
            ("export_jobtype", "Can export job_type"),
            ("view_activity_jobtype", "Can view job_type activity"),
        )


pre_save.connect(slugify_name, sender=JobType)
