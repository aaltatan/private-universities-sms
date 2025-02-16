from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from apps.core.models import AbstractUniqueNameModel
from apps.core.schemas import Report
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search

from ..constants import governorates as constants


class GovernorateManager(models.Manager):
    def get_report_cities_count(
        self,
        include_zeros: bool = False,
        qs: QuerySet | None = None,
    ) -> Report:
        """
        Returns a queryset of governorates with the number of cities in each.
        """
        if qs is None:
            qs = self.get_queryset()

        report = qs.values("name").annotate(
            counts=models.Count("cities"),
        )

        if not include_zeros:
            report = report.filter(counts__gt=0)

        report_schema = Report(
            title=_("governorates count"),
            headers=[_("name"), _("counts")],
            report=list(report),
        )

        return report_schema

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("cities")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Governorate(AbstractUniqueNameModel):
    objects: GovernorateManager = GovernorateManager()

    class Meta:
        ordering = ("name",)
        permissions = (
            ("export_governorate", "Can export governorate"),
            ("view_activity_governorate", "Can view governorate activity"),
        )


pre_save.connect(slugify_name, sender=Governorate)
