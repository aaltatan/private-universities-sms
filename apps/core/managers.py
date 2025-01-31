from django.db import models


class ActivityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("user")
