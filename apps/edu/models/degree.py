from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search

from ..constants import degrees as constants


class DegreeManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Degree(AbstractUniqueNameModel):
    class AcademicChoices(models.TextChoices):
        ACADEMIC = True, _("academic").title()
        APPLIED = False, _("applied").title()

    order = models.IntegerField(
        verbose_name=_("order"),
        help_text=_("order of degree"),
        default=1,
    )
    is_academic = models.BooleanField(
        verbose_name=_("is academic"),
        default=True,
        help_text=_("is an academic degree"),
    )

    objects: DegreeManager = DegreeManager()

    class Meta:
        icon = "square-3-stack-3d"
        codename_plural = 'degrees'
        verbose_name = _("degree").title()
        verbose_name_plural = _("degrees").title()
        ordering = ("-is_academic", "order", "name")
        permissions = (
            ("export_degree", "Can export degree"),
            ("view_activity_degree", "Can view degree activity"),
        )


pre_save.connect(slugify_name, sender=Degree)
