from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name
from apps.core.utils import annotate_search

from ..constants import nationalities as constants


class NationalityManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                search=annotate_search(constants.SEARCH_FIELDS),
            )
        )


class Nationality(AbstractUniqueNameModel):
    class IS_LOCAL_CHOICES(models.TextChoices):
        LOCAL = True, _("local").title()
        FOREIGN = False, _("foreign").title()

    is_local = models.BooleanField(
        verbose_name=_("is local"),
        default=False,
        help_text=_("is it local or foreign"),
    )

    objects: NationalityManager = NationalityManager()

    def save(self, *args, **kwargs):
        Model = self.__class__
        objs = []

        if self.is_local:
            qs = Model.objects.exclude(pk=self.pk)
            for obj in qs:
                obj.is_local = False
                objs.append(obj)

            Model.objects.bulk_update(objs, ["is_local"])

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "nationalities"
        permissions = (
            ("export_nationality", "Can export nationality"),
            ("view_activity_nationality", "Can view nationality activity"),
        )


pre_save.connect(slugify_name, sender=Nationality)
