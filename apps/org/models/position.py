from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import positions as constants


class PositionManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Position(AbstractUniqueNameModel):
    order = models.IntegerField(
        verbose_name=_('order'),
        help_text=_('order of position'),
        default=1,
    )

    objects: PositionManager = PositionManager()

    class Meta:
        icon = "chevron-double-up"
        codename_plural = "positions"
        verbose_name = _("position").title()
        verbose_name_plural = _("positions").title()
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
