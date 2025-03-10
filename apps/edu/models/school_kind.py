from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import school_kinds as constants


class SchoolKindManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("schools")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
                schools_count=models.Count("schools"),
            )
        )


class SchoolKind(AbstractUniqueNameModel):
    class OwnershipChoices(models.TextChoices):
        GOVERNMENTAL = True, _("governmental").title()
        PRIVATE = False, _("private").title()

    class VirtualChoices(models.TextChoices):
        VIRTUAL = True, _("virtual").title()
        ORDINARY = False, _("ordinary").title()

    is_governmental = models.BooleanField(
        verbose_name=_("is governmental"),
        default=True,
        help_text=_("is it governmental or private"),
    )
    is_virtual = models.BooleanField(
        verbose_name=_("is virtual"),
        default=False,
        help_text=_("is it virtual or ordinary"),
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
