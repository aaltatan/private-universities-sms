from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from apps.core.models import AbstractUniqueNameModel
from apps.core.schemas import ReportSchema
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search

from ..constants import governorates as constants


class GovernorateManager(models.Manager):
    def get_report_cities_count(self, include_zeros=False) -> ReportSchema:
        """
        Returns a queryset of governorates with the number of cities in each.
        """
        report = (
            self.get_queryset()
            .values("name")
            .annotate(
                counts=models.Count("cities"),
            )
        )
        if not include_zeros:
            report = report.filter(counts__gt=0)

        report_schema = ReportSchema(
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
                cities_count=models.Count("cities"),
            )
        )


class Governorate(AbstractUniqueNameModel):
    objects: GovernorateManager = GovernorateManager()

    class Meta:
        icon = "home-modern"
        ordering = ("name",)
        codename_plural = "governorates"
        verbose_name = _("governorate").title()
        verbose_name_plural = _("governorates").title()
        permissions = (
            ("export_governorate", "Can export governorate"),
            ("view_activity_governorate", "Can view governorate activity"),
        )


pre_save.connect(slugify_name, sender=Governorate)
