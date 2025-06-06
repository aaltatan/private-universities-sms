from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import AbstractUniqueNameModel
from apps.core.utils import annotate_search

from ..constants import degrees as constants


class DegreeManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
                employees_count=models.Count("employees"),
            )
        )


class Degree(AddCreateActivityMixin, AbstractUniqueNameModel):
    class AcademicChoices(models.TextChoices):
        ACADEMIC = True, _("academic").title()
        APPLIED = False, _("applied").title()

    order = models.IntegerField(
        verbose_name=_("order"),
        help_text=_(
            "for sorting purposes, you can use the same order for different degrees"
        ),
        default=1,
    )
    is_academic = models.BooleanField(
        verbose_name=_("is academic"),
        default=True,
    )

    objects: DegreeManager = DegreeManager()

    class Meta:
        icon = "square-3-stack-3d"
        codename_plural = "degrees"
        verbose_name = _("degree").title()
        verbose_name_plural = _("degrees").title()
        ordering = ("-is_academic", "order", "name")
        permissions = (
            ("export_degree", "Can export degree"),
            ("view_activity_degree", "Can view degree activity"),
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = ("name", "is_academic", "description")


pre_save.connect(signals.slugify_name, sender=Degree)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Degree)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Degree)
