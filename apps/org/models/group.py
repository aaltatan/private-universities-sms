from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import groups as constants


class GroupManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
                employees_count=models.Count("employees"),
            )
        )


class Group(AddCreateActivityMixin, AbstractUniqueNameModel):
    class KindChoices(models.TextChoices):
        ACADEMIC = "academic", _("academic").title()
        ADMINISTRATIVE = "administrative", _("administrative").title()

    kind = models.CharField(
        max_length=50,
        choices=KindChoices.choices,
        default=KindChoices.ADMINISTRATIVE,
    )
    objects: GroupManager = GroupManager()

    class Meta:
        icon = "user-group"
        codename_plural = "groups"
        verbose_name = _("group").title()
        verbose_name_plural = _("groups").title()
        ordering = ("kind", "name")
        permissions = (
            ("export_group", "Can export group"),
            ("view_activity_group", "Can view group activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", "kind", "description")


pre_save.connect(signals.slugify_name, sender=Group)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Group)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Group)
