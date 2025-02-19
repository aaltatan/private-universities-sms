from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
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
        verbose_name=_('payable'),
        help_text=_('payable'),
        default=True,
    )

    objects: StatusManager = StatusManager()

    class Meta:
        ordering = ("is_payable", "name")
        verbose_name_plural = _("statuses")
        permissions = (
            ("export_status", "Can export status"),
            ("view_activity_status", "Can view status activity"),
        )


pre_save.connect(slugify_name, sender=Status)
