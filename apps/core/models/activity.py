from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from .user import User
from ..managers import ActivityManager


class Activity(models.Model):
    class KindChoices(models.TextChoices):
        CREATE = "create", _("create").title()
        UPDATE = "update", _("update").title()
        DELETE = "delete", _("delete").title()
        EXPORT = "export", _("export").title()
        OTHER = "other", _("other").title()

    created_at = models.DateTimeField(
        auto_now=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="activities",
    )
    kind = models.CharField(
        max_length=255,
        choices=KindChoices.choices,
        default=KindChoices.OTHER,
    )
    data = models.JSONField(
        null=True,
        blank=True,
    )
    notes = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )

    objects = ActivityManager()

    def __str__(self) -> str:
        return f"Activity[{self.kind}] @{self.user.username}"
    
    def save(self, *args, **kwargs) -> None:
        if self.kind == self.KindChoices.CREATE:
            self.notes = str(self.content_object)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "kind"]
        verbose_name_plural = "activities"
