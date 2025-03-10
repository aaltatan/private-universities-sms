from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import statuses as constants


class StatusManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Status(AbstractUniqueNameModel):
    class PayableChoices(models.TextChoices):
        PAYABLE = True, _("payable").title()
        NOT_PAYABLE = False, _("not payable").title()

    is_payable = models.BooleanField(
        verbose_name=_("payable"),
        help_text=_("payable"),
        default=True,
    )

    objects: StatusManager = StatusManager()

    class Meta:
        icon = "check-circle"
        ordering = ("is_payable", "name")
        codename_plural = "statuses"
        verbose_name = _("status").title()
        verbose_name_plural = _("statuses").title()
        permissions = (
            ("export_status", "Can export status"),
            ("view_activity_status", "Can view status activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ("name", "is_payable", "description")


pre_save.connect(signals.slugify_name, sender=Status)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Status)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Status)
