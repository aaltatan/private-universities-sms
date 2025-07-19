from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import school_kinds as constants


class SchoolKindQuerySet(models.QuerySet):
    def annotate_employees_count(self):
        return self.annotate(
            employees_count=models.Count("schools__employees", distinct=True),
        )

    def annotate_schools_count(self):
        return self.annotate(
            schools_count=models.Count("schools", distinct=True),
        )


class SchoolKindManager(models.Manager):
    def annotate_employees_count(self):
        return self.get_queryset().annotate_employees_count()

    def annotate_schools_count(self):
        return self.get_queryset().annotate_schools_count()

    def get_queryset(self):
        queryset = SchoolKindQuerySet(self.model, using=self._db)
        return queryset.annotate(
            search=annotate_search(constants.SEARCH_FIELDS),
        )


class SchoolKind(AddCreateActivityMixin, AbstractUniqueNameModel):
    class OwnershipChoices(models.TextChoices):
        GOVERNMENTAL = True, _("governmental").title()
        PRIVATE = False, _("private").title()

    class VirtualChoices(models.TextChoices):
        VIRTUAL = True, _("virtual").title()
        ORDINARY = False, _("ordinary").title()

    is_governmental = models.BooleanField(
        verbose_name=_("is governmental"),
        default=True,
    )
    is_virtual = models.BooleanField(
        verbose_name=_("is virtual"),
        default=False,
    )

    objects: SchoolKindManager = SchoolKindManager()

    class Meta:
        icon = "academic-cap"
        ordering = ("name",)
        codename_plural = "school_kinds"
        verbose_name = _("school kind").title()
        verbose_name_plural = _("school kinds").title()
        permissions = (
            ("export_schoolkind", "Can export school kind"),
            ("view_activity_schoolkind", "Can view school kind activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolKind
        fields = ("name", "is_governmental", "is_virtual", "description")


pre_save.connect(signals.slugify_name, sender=SchoolKind)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=SchoolKind)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=SchoolKind)
