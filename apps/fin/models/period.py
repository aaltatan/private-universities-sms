from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.querysets import JournalsTotalsQuerysetMixin
from apps.core.utils import annotate_search

from ..constants import periods as constants
from .year import Year


class PeriodQuerySet(JournalsTotalsQuerysetMixin["PeriodQuerySet"], models.QuerySet):
    pass


class PeriodManager(models.Manager):
    def get_queryset(self):
        queryset = PeriodQuerySet(self.model, using=self._db)
        return queryset.select_related("year").annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )

    def annotate_journals_total_debit(
        self,
        sum_filter_Q: models.Q | None = None,
    ):
        return self.get_queryset().annotate_journals_total_debit(sum_filter_Q)

    def annotate_journals_total_credit(
        self,
        sum_filter_Q: models.Q | None = None,
    ):
        return self.get_queryset().annotate_journals_total_credit(sum_filter_Q)

    def annotate_journals_total_amount(
        self,
        sum_filter_Q: models.Q | None = None,
    ):
        return self.get_queryset().annotate_journals_total_amount(sum_filter_Q)


class Period(AddCreateActivityMixin, AbstractUniqueNameModel):
    class ClosedChoices(models.TextChoices):
        CLOSED = True, _("closed").title()
        OPEN = False, _("open").title()

    year = models.ForeignKey(
        Year,
        verbose_name=_("year"),
        on_delete=models.PROTECT,
        related_name="periods",
    )
    start_date = models.DateField(
        verbose_name=_("start date"),
    )
    is_closed = models.BooleanField(
        default=False,
        verbose_name=_("is closed"),
    )

    objects: PeriodManager = PeriodManager()

    class Meta:
        icon = "calendar-date-range"
        ordering = ("start_date",)
        codename_plural = "periods"
        verbose_name = _("period").title()
        verbose_name_plural = _("periods").title()
        permissions = (
            ("export_period", "Can export period"),
            ("view_activity_period", "Can view period activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    year = serializers.CharField(source="year.name")

    class Meta:
        model = Period
        fields = ("name", "year", "start_date", "is_closed", "description")


pre_save.connect(signals.slugify_name, sender=Period)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Period)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Period)
