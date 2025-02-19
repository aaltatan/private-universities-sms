from django.db import models
from django.db.models import options
from django.urls import reverse
from django.utils.translation import gettext as _

from ..validators import four_char_length_validator

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ("icon", "title")


class AbstractUniqueNameModel(models.Model):
    """
    Abstract model for models that have a unique name field and a slug field and optional description field.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[four_char_length_validator],
    )
    description = models.TextField(
        default="",
        blank=True,
        null=True,
        verbose_name=_("description"),
    )
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

    def get_activities_url(self) -> str:
        app_label: str = self.__get_app_label()
        model_name: str = self.__get_model_name()

        base_url = reverse("core:activities", kwargs={"object_id": self.pk})

        return f"{base_url}?app_label={app_label}&model={model_name}"

    def get_delete_url(self) -> str:
        verbose_name_plural: str = self.__get_verbose_name_plural()
        return reverse(
            f"{verbose_name_plural}:delete",
            kwargs={"slug": self.slug},
        )

    def get_update_url(self) -> str:
        verbose_name_plural: str = self.__get_verbose_name_plural()
        return reverse(
            f"{verbose_name_plural}:update",
            kwargs={"slug": self.slug},
        )

    def __get_verbose_name_plural(self) -> str:
        return self._meta.verbose_name_plural

    def __get_app_label(self) -> str:
        return self._meta.app_label

    def __get_model_name(self) -> str:
        return self._meta.model_name
