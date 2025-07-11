from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals, validators
from apps.core.mixins import AddCreateActivityMixin

from .employee import Employee


class MobileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("employee")


class Mobile(AddCreateActivityMixin, models.Model):
    class HasWhatsappChoices(models.TextChoices):
        NONE = "", "------"
        YES = True, _("yes").title()
        NO = False, _("no").title()

    class KindChoices(models.TextChoices):
        PERSONAL = "personal", _("personal").title()
        WORK = "work", _("work").title()
        OTHER = "other", _("other").title()

    number = models.CharField(
        max_length=255,
        verbose_name=_("mobile number"),
        validators=[validators.syrian_mobile_validator],
        unique=True,
    )
    kind = models.CharField(
        max_length=30,
        choices=KindChoices.choices,
        default=KindChoices.PERSONAL,
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="mobiles",
    )
    has_whatsapp = models.BooleanField(
        default=True,
        verbose_name=_("has whatsapp"),
    )
    ordering = models.PositiveIntegerField(
        default=0,
    )
    notes = models.TextField(
        verbose_name=_("notes"),
        max_length=1000,
        default="",
        blank=True,
    )

    objects: MobileManager = MobileManager()

    def __str__(self) -> str:
        return f"+963 {self.number[1:4]} {self.number[4:7]} {self.number[7:]}"

    def get_absolute_url(self) -> str:
        return f"tel:+963{self.number[1:]}"

    def get_whatsapp_url(self) -> str:
        return f"https://web.whatsapp.com/send?phone=+963{self.number[1:]}&text=Hello!"

    class Meta:
        verbose_name = _("mobile")
        verbose_name_plural = _("mobiles")
        ordering = ("kind", "number")
        codename_plural = "mobiles"


class ActivitySerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source="employee.fullname")

    class Meta:
        model = Mobile
        fields = ("number", "kind", "employee", "has_whatsapp")


pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Mobile)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Mobile)
