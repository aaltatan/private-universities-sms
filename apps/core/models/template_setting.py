from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from .template import Template


class TemplateSetting(models.Model):
    voucher = models.OneToOneField(
        Template,
        on_delete=models.PROTECT,
        related_name="template_settings",
        verbose_name=_("setting"),
    )

    @classmethod
    def get_voucher_template(cls):
        return cls.objects.first().voucher.file

    def __str__(self):
        return f"VoucherSetting(voucher={self.voucher})"

    def clean(self):
        Klass = self.__class__
        if Klass.objects.count() >= 1:
            raise ValidationError(_("only one setting allowed"))

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.clean()
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _("template setting").title()
        verbose_name_plural = _("template settings").title()
        ordering = ("voucher__name",)
