from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search
from apps.geo.models import Nationality

from ..constants import schools as constants


class SchoolManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("nationality")
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class School(AbstractUniqueNameModel):
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
    nationality = models.ForeignKey(
        Nationality,
        on_delete=models.PROTECT,
        related_name="schools",
        verbose_name=_("nationality"),
    )
    website = models.URLField(
        verbose_name=_("website"),
        max_length=255,
        default="",
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name=_("email"),
        max_length=255,
        default="",
        blank=True,
        null=True,
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
        title = _("schools")
        ordering = ("name",)
        verbose_name_plural = "schools"
        permissions = (
            ("export_school", "Can export school"),
            ("view_activity_school", "Can view school activity"),
        )


pre_save.connect(slugify_name, sender=School)
