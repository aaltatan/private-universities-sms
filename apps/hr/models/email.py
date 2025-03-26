from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin

from .employee import Employee


class EmailManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("employee")


class Email(AddCreateActivityMixin, models.Model):
    class KindChoices(models.TextChoices):
        PERSONAL = "personal", _("personal").title()
        WORK = "work", _("work").title()
        OTHER = "other", _("other").title()

    email = models.EmailField(
        max_length=255,
        verbose_name=_("email"),
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
        related_name="emails",
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

    objects: EmailManager = EmailManager()

    def __str__(self) -> str:
        return self.email

    def get_absolute_url(self) -> str:
        return f"mailto:{self.email}"

    class Meta:
        verbose_name = _("email")
        verbose_name_plural = _("emails")
        ordering = ("kind", "email")
        codename_plural = "emails"


class ActivitySerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()

    def get_employee(self, obj: Email):
        return obj.employee.get_fullname()

    class Meta:
        model = Email
        fields = ("email", "kind", "employee")


pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Email)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Email)
