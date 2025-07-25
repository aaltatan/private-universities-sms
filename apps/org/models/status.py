from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.querysets import (
    EmployeesCountManagerMixin,
    EmployeesCountQuerysetMixin,
)
from apps.core.utils import annotate_search

from ..constants import statuses as constants


class StatusQuerySet(
    EmployeesCountQuerysetMixin["StatusQuerySet"],
    models.QuerySet,
):
    pass


class StatusManager(EmployeesCountManagerMixin[StatusQuerySet], models.Manager):
    def get_queryset(self):
        queryset = StatusQuerySet(self.model, using=self._db)
        return queryset.annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )


class Status(AddCreateActivityMixin, AbstractUniqueNameModel):
    class PayableChoices(models.TextChoices):
        PAYABLE = True, _("payable").title()
        NOT_PAYABLE = False, _("not payable").title()

    class SeparatedChoices(models.TextChoices):
        SEPARATED = True, _("separated").title()
        NOT_SEPARATED = False, _("not separated").title()

    is_payable = models.BooleanField(
        verbose_name=_("is payable"),
        default=True,
    )
    is_separated = models.BooleanField(
        verbose_name=_("is separated"),
        default=False,
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


def pre_save_status(sender, instance: Status, *args, **kwargs):
    if instance.is_separated:
        instance.is_payable = False


pre_save.connect(signals.slugify_name, sender=Status)
pre_save.connect(pre_save_status, sender=Status)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Status)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Status)
