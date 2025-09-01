from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search
from apps.geo.models import Nationality
from apps.core.querysets import (
    EmployeesCountQuerysetMixin,
    EmployeesCountManagerMixin,
)

from ..constants import schools as constants
from .school_kind import SchoolKind


class SchoolQuerySet(
    EmployeesCountQuerysetMixin["SchoolQuerySet"],
    models.QuerySet,
):
    pass


class SchoolManager(EmployeesCountManagerMixin[SchoolQuerySet], models.Manager):
    def get_queryset(self):
        queryset = SchoolQuerySet(self.model, using=self._db)
        return queryset.select_related("nationality", "kind").annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
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
    address = models.CharField(
        verbose_name=_("address"),
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
        verbose_name = _("school")
        verbose_name_plural = _("schools")
        permissions = (
            ("export_school", "Can export school"),
            ("view_activity_school", "Can view school activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    nationality = serializers.CharField(source="nationality.name")
    kind = serializers.CharField(source="kind.name")

    class Meta:
        model = School
        fields = (
            "name",
            "nationality",
            "kind",
            "website",
            "email",
            "phone",
            "address",
            "description",
        )


pre_save.connect(signals.slugify_name, sender=School)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=School)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=School)
