from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.querysets import (
    EmployeesCountQuerysetMixin,
    EmployeesCountManagerMixin,
)
from apps.core.utils import annotate_search

from ..constants import positions as constants


class PositionQuerySet(
    EmployeesCountQuerysetMixin["PositionQuerySet"],
    models.QuerySet,
):
    pass


class PositionManager(
    EmployeesCountManagerMixin[PositionQuerySet],
    models.Manager,
):
    def get_queryset(self):
        queryset = PositionQuerySet(self.model, using=self._db)
        return queryset.annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )


class Position(AddCreateActivityMixin, AbstractUniqueNameModel):
    order = models.IntegerField(
        verbose_name=_("order"),
        help_text=_(
            "for sorting purposes, you can use the same order for different positions"
        ),
        default=1,
    )

    objects: PositionManager = PositionManager()

    class Meta:
        icon = "chevron-double-up"
        codename_plural = "positions"
        verbose_name = _("position")
        verbose_name_plural = _("positions")
        ordering = ("order", "name")
        permissions = (
            ("export_position", "Can export position"),
            ("view_activity_position", "Can view position activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ("name", "order", "description")


pre_save.connect(signals.slugify_name, sender=Position)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Position)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Position)
