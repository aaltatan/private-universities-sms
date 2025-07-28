from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import options
from django.urls import reverse
from django.utils.translation import gettext as _

from .. import validators

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ("icon", "codename_plural")


class SingletonModelMixin:
    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        raise ValidationError(_("you cannot delete this object"))

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if self.pk is None:
            raise ValidationError(_("you cannot multiple templates"))
        return super().save(force_insert, force_update, using, update_fields)


class UrlsMixin:
    def get_activities_url(self) -> str:
        app_label: str = self.__get_app_label()
        model_name: str = self.__get_model_name()

        base_url = reverse("core:activities", kwargs={"object_id": self.pk})

        return f"{base_url}?app_label={app_label}&model={model_name}"

    def get_absolute_url(self) -> str:
        app_label = self.__get_app_label()
        codename_plural: str = self.__get_codename_plural()
        return reverse(
            f"{app_label}:{codename_plural}:details",
            kwargs={"slug": self.slug},
        )

    def get_delete_url(self) -> str:
        app_label = self.__get_app_label()
        codename_plural: str = self.__get_codename_plural()
        return reverse(
            f"{app_label}:{codename_plural}:delete",
            kwargs={"slug": self.slug},
        )

    def get_update_url(self) -> str:
        app_label = self.__get_app_label()
        codename_plural: str = self.__get_codename_plural()
        return reverse(
            f"{app_label}:{codename_plural}:update",
            kwargs={"slug": self.slug},
        )

    def __get_codename_plural(self) -> str:
        return self._meta.codename_plural

    def __get_app_label(self) -> str:
        return self._meta.app_label

    def __get_model_name(self) -> str:
        return self._meta.model_name


class AbstractUniqueNameModel(UrlsMixin, models.Model):
    """
    Abstract model for models that have a unique name field and a slug field and optional description field.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[validators.four_char_length_validator],
        verbose_name=_("name"),
    )
    description = models.TextField(
        default="",
        blank=True,
        null=True,
        verbose_name=_("description"),
    )
    ordering = models.PositiveIntegerField(default=0)  # to order objects in inlines
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        default=None,
        allow_unicode=True,
    )

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteAbstractModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, permanent=False):
        if permanent:
            super().delete(using=using, keep_parents=keep_parents)
        else:
            self.is_deleted = True
            self.save()
