from django.db import models
from django.db.models.signals import pre_save

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search

from ..constants import groups as constants


class GroupManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Group(AbstractUniqueNameModel):
    objects: GroupManager = GroupManager()

    class Meta:
        ordering = ("name",)
        permissions = (
            ("export_group", "Can export group"),
            ("view_activity_group", "Can view group activity"),
        )


pre_save.connect(slugify_name, sender=Group)
