from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.schemas import ReportSchema
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
                job_subtypes_count=models.Count("job_subtypes", distinct=True),
                employees_count=models.Count("job_subtypes__employees", distinct=True),
            )
        )


class JobType(AddCreateActivityMixin, AbstractUniqueNameModel):
    objects: JobTypeManager = JobTypeManager()

    class Meta:
        icon = "briefcase"
        codename_plural = "job_types"
        verbose_name = _("job type").title()
        verbose_name_plural = _("job types").title()
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
