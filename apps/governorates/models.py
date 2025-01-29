from django.db.models.signals import pre_save

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name

from .managers import GovernorateManager


class Governorate(AbstractUniqueNameModel):
    objects = GovernorateManager()

    class Meta:
        ordering = ("name",)
        permissions = (("export_governorate", "Can export governorate"),)


pre_save.connect(slugify_name, sender=Governorate)
