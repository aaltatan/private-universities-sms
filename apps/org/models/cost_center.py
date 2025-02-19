from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search
from apps.core.validators import numeric_validator

from ..constants import cost_centers as constants


class CostCenterManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class CostCenter(AbstractUniqueNameModel):
    accounting_id = models.CharField(
        verbose_name=_("cost center id"),
        validators=[numeric_validator],
        unique=True,
        help_text=_("cost center id in accounting system"),
        max_length=10,
    )

    objects: CostCenterManager = CostCenterManager()

    class Meta:
        icon = "building-office-2"
        title = _("cost centers")
        ordering = ("accounting_id", "name")
        verbose_name_plural = "cost_centers"
        permissions = (
            ("export_costcenter", "Can export cost center"),
            ("view_activity_costcenter", "Can view cost center activity"),
        )


pre_save.connect(slugify_name, sender=CostCenter)
