from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals, validators
from apps.core.mixins import AddCreateActivityMixin

from .employee import Employee


class PhoneManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("employee")


class Phone(AddCreateActivityMixin, models.Model):
    class KindChoices(models.TextChoices):
        PERSONAL = "personal", _("personal").title()
        WORK = "work", _("work").title()
        OTHER = "other", _("other").title()

    number = models.CharField(
        max_length=255,
        verbose_name=_("phone number"),
        validators=[validators.syrian_phone_validator],
    )
    kind = models.CharField(
        max_length=30,
        choices=KindChoices.choices,
        default=KindChoices.PERSONAL,
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="phones",
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

    objects: PhoneManager = PhoneManager()

    def __str__(self) -> str:
        return f"+963{self.number[1:]}"

    def get_absolute_url(self) -> str:
        return f"tel:+963{self.number[1:]}"

    class Meta:
        unique_together = ("employee", "number")
        verbose_name = _("phone")
        verbose_name_plural = _("phones")
        ordering = ("kind", "number")
        codename_plural = "phones"


class ActivitySerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source="employee.fullname")

    class Meta:
        model = Phone
        fields = ("number", "kind", "employee")


pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Phone)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Phone)
