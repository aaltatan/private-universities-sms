from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from apps.core.models import AbstractUniqueNameModel
from apps.core.signals import slugify_name

from . import managers


class Governorate(AbstractUniqueNameModel):
    objects = managers.GovernorateManager()

    class Meta:
        ordering = ("name",)
        permissions = (
            ("export_governorate", "Can export governorate"),
            ("view_activity_governorate", "Can view governorate activity"),
        )


class City(AbstractUniqueNameModel):
    governorate = models.ForeignKey(
        Governorate,
        on_delete=models.PROTECT,
        related_name="cities",
    )

    objects = managers.CityManager()

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "cities"
        permissions = (
            ("export_city", "Can export city"),
            ("view_activity_city", "Can view city activity"),
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

    objects = managers.NationalityManager()

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


pre_save.connect(slugify_name, sender=City)
pre_save.connect(slugify_name, sender=Governorate)
pre_save.connect(slugify_name, sender=Nationality)
