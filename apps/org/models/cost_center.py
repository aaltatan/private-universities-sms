from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.models import AbstractUniqueNameModel
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
        ordering = ("accounting_id", "name")
        codename_plural = "cost_centers"
        verbose_name = _("cost center").title()
        verbose_name_plural = _("cost centers").title()
        permissions = (
            ("export_costcenter", "Can export cost center"),
            ("view_activity_costcenter", "Can view cost center activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = ("name", "accounting_id", "description")


pre_save.connect(signals.slugify_name, sender=CostCenter)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=CostCenter)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=CostCenter)
