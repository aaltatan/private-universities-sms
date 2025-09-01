from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import User
from ..managers import ActivityManager


class Activity(models.Model):
    class KindChoices(models.TextChoices):
        CREATE = "create", _("create")
        UPDATE = "update", _("update")
        DELETE = "delete", _("delete")
        EXPORT = "export", _("export")
        OTHER = "other", _("other")

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
        codename_plural = "activities"
        verbose_name = _("activity")
        verbose_name_plural = _("activities")
