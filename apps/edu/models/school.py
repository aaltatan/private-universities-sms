from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search
from apps.geo.models import Nationality

from ..constants import schools as constants
from .school_kind import SchoolKind


class SchoolManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("nationality", "kind")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class School(AddCreateActivityMixin, AbstractUniqueNameModel):
    nationality = models.ForeignKey(
        Nationality,
        on_delete=models.PROTECT,
        related_name="schools",
        verbose_name=_("nationality"),
    )
    kind = models.ForeignKey(
        SchoolKind,
        on_delete=models.PROTECT,
        related_name="schools",
        verbose_name=_("kind"),
    )
    website = models.URLField(
        verbose_name=_("website"),
        max_length=255,
        default="",
        blank=True,
        null=True,
        unique=True,
    )
    email = models.EmailField(
        verbose_name=_("email"),
        max_length=255,
        default="",
        blank=True,
        null=True,
        unique=True,
    )
    phone = models.CharField(
        verbose_name=_("phone"),
        max_length=255,
        default="",
        blank=True,
        null=True,
    )

    objects: SchoolManager = SchoolManager()

    class Meta:
        icon = "academic-cap"
        ordering = ("name",)
        codename_plural = "schools"
        verbose_name = _("school").title()
        verbose_name_plural = _("schools").title()
        permissions = (
            ("export_school", "Can export school"),
            ("view_activity_school", "Can view school activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    nationality = serializers.CharField(source="nationality.name")
    kind = serializers.CharField(source="kind.name")

    class Meta:
        model = School
        fields = ("name", "nationality", "kind", "description")


pre_save.connect(signals.slugify_name, sender=School)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=School)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=School)
