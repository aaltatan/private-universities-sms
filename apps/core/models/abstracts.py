from django.db import models
from django.urls import reverse

from ..validators import four_char_length_validator


class AbstractUniqueNameModel(models.Model):
    """
    Abstract model for models that have a unique name field and a slug field and optional description field.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[four_char_length_validator],
    )
    description = models.TextField(default="", blank=True, null=True)
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

    def get_delete_url(self) -> str:
        app_label: str = self.__get_app_label()
        return reverse(
            f"{app_label}:delete",
            kwargs={"slug": self.slug},
        )

    def get_update_url(self) -> str:
        app_label: str = self.__get_app_label()
        return reverse(
            f"{app_label}:update",
            kwargs={"slug": self.slug},
        )

    def __get_app_label(self) -> str:
        return self._meta.verbose_name_plural
