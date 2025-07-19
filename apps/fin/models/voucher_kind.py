from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import voucher_kinds as constants


class VoucherKindQuerySet(models.QuerySet):
    def annotate_vouchers_count(self):
        return self.annotate(
            vouchers_count=models.Count(
                "vouchers",
                distinct=True,
                filter=models.Q(vouchers__is_deleted=False),
            ),
        )


class VoucherKindManager(models.Manager):
    def annotate_vouchers_count(self):
        return self.get_queryset().annotate_vouchers_count()

    def get_queryset(self):
        queryset = VoucherKindQuerySet(self.model, using=self._db)
        return queryset.annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )


class VoucherKind(AddCreateActivityMixin, AbstractUniqueNameModel):
    objects: VoucherKindManager = VoucherKindManager()

    class Meta:
        icon = "rectangle-group"
        ordering = ("name",)
        codename_plural = "voucher_kinds"
        verbose_name = _("voucher kind").title()
        verbose_name_plural = _("voucher kinds").title()
        permissions = (
            ("export_voucherkind", "Can export voucher kind"),
            ("view_activity_voucherkind", "Can view voucher kind activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherKind
        fields = ("name", "description")


pre_save.connect(signals.slugify_name, sender=VoucherKind)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=VoucherKind)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=VoucherKind)
