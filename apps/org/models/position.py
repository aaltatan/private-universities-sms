from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
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
        ordering = ("order", "name")
        permissions = (
            ("export_position", "Can export position"),
            ("view_activity_position", "Can view position activity"),
        )


pre_save.connect(slugify_name, sender=Position)
