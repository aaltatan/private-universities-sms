import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.core import signals, validators
from apps.core.choices import MonthChoices, QuarterChoices
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import SoftDeleteAbstractModel, TimeStampAbstractModel, User
from apps.core.models.abstracts import UrlsMixin
from apps.fin.models import Period, VoucherKind

from ..managers import VoucherManager, VoucherProxyManager


class Voucher(
    UrlsMixin,
    AddCreateActivityMixin,
    SoftDeleteAbstractModel,
    TimeStampAbstractModel,
):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    voucher_serial = models.CharField(
        max_length=20,
        verbose_name=_("voucher serial"),
        unique=True,
        editable=False,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="vouchers",
        verbose_name=_("user"),
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="updated_vouchers",
        verbose_name=_("updated by"),
        blank=True,
        null=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    # basics
    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
    )
    date = models.DateField(
        verbose_name=_("date"),
    )
    # classification
    kind = models.ForeignKey(
        VoucherKind,
        on_delete=models.PROTECT,
        verbose_name=_("kind"),
        related_name="vouchers",
    )
    month = models.CharField(
        max_length=255,
        choices=MonthChoices.choices,
        default=MonthChoices.JANUARY,
        verbose_name=_("month"),
    )
    quarter = models.CharField(
        max_length=255,
        choices=QuarterChoices.choices,
        default=QuarterChoices.Q1,
        verbose_name=_("quarter"),
    )
    period = models.ForeignKey(
        Period,
        on_delete=models.PROTECT,
        verbose_name=_("period"),
        related_name="vouchers",
    )
    # organization
    notes = models.TextField(
        verbose_name=_("notes"),
        default="",
        blank=True,
    )
    serial_id = models.CharField(
        max_length=255,
        verbose_name=_("serial id"),
        default="",
        blank=True,
        help_text=_("dewan id if exists"),
    )
    serial_date = models.DateField(
        verbose_name=_("serial date"),
        blank=True,
        null=True,
        help_text=_("dewan date if exists"),
    )
    approve_date = models.DateField(
        verbose_name=_("approve date"),
        blank=True,
        null=True,
        help_text=_("date of approve by vouchers orderer (signature)"),
    )
    due_date = models.DateField(
        verbose_name=_("due date"),
        blank=True,
        null=True,
    )
    document = models.FileField(
        upload_to="vouchers",
        verbose_name=_("document"),
        blank=True,
        null=True,
        validators=[
            validators.pdf_image_extension_validator,
            validators.validate_pdf_image_mimetype,
        ],
    )
    accounting_journal_sequence = models.CharField(
        max_length=255,
        verbose_name=_("accounting journal sequence"),
        blank=True,
        default="",
        help_text=_(
            "the sequence of the accounting journal in accounting system e.g. JOV0001"
        ),
    )
    # functional
    is_audited = models.BooleanField(
        default=False,
        verbose_name=_("is audited"),
    )
    audited_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="audited_vouchers",
        verbose_name=_("audited by"),
        blank=True,
        null=True,
    )
    is_migrated = models.BooleanField(
        default=False,
        verbose_name=_("is migrated"),
    )

    objects: VoucherManager = VoucherManager()
    all_objects: VoucherProxyManager = VoucherProxyManager()

    def delete(self, using=None, keep_parents=False, permanent=False):
        super().delete(using, keep_parents, permanent)
        self.document.delete()

    def clean(self):
        if self.due_date and self.due_date < self.date:
            raise ValidationError(
                _("due date cannot be earlier than date"),
            )

        if self.approve_date and self.approve_date > self.date:
            raise ValidationError(
                _("approve date cannot be later than date"),
            )

    def get_absolute_url(self):
        return super().get_absolute_url()

    def get_audit_url(self):
        return reverse(
            "trans:vouchers:audit",
            kwargs={"slug": self.slug},
        )

    def __str__(self):
        return f"{self.title} ({self.voucher_serial})"

    class Meta:
        icon = "document-check"
        ordering = ("-date", "-created_at", "voucher_serial")
        codename_plural = "vouchers"
        verbose_name = _("voucher").title()
        verbose_name_plural = _("vouchers").title()
        permissions = (
            ("export_voucher", "Can export voucher"),
            ("migrate_voucher", "Can migrate voucher"),
            ("unmigrate_voucher", "Can unmigrate voucher"),
            ("audit_voucher", "Can audit voucher"),
            ("unaudit_voucher", "Can unaudit voucher"),
            ("view_activity_voucher", "Can view voucher activity"),
        )


class VoucherProxy(Voucher):
    objects: VoucherProxyManager = VoucherProxyManager()

    class Meta:
        proxy = True
        verbose_name = _("voucher proxy")
        verbose_name_plural = _("all vouchers")
        codename_plural = "proxy_vouchers"


class ActivitySerializer(serializers.ModelSerializer):
    kind = serializers.CharField(source="kind.name")
    period = serializers.CharField(source="period.name")
    audited_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_updated_by(self, obj):
        return obj.updated_by.username if obj.updated_by else ""

    def get_audited_by(self, obj):
        return obj.audited_by.username if obj.audited_by else ""

    class Meta:
        model = Voucher
        fields = (
            "updated_by",
            "title",
            "date",
            "kind",
            "month",
            "quarter",
            "period",
            "notes",
            "serial_id",
            "serial_date",
            "approve_date",
            "due_date",
            "document",
            "accounting_journal_sequence",
            "is_audited",
            "audited_by",
            "is_migrated",
            "is_deleted",
        )


def slugify_voucher(sender, instance: Voucher, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(
            f"{instance.voucher_serial}-{instance.title}",
            allow_unicode=True,
        )


def generate_voucher_serial(sender, instance: Voucher, *args, **kwargs):
    Klass = instance.__class__
    if not instance.voucher_serial:
        instance.voucher_serial = Klass.all_objects.get_next_voucher_serial()


pre_save.connect(generate_voucher_serial, sender=Voucher)
pre_save.connect(slugify_voucher, sender=Voucher)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Voucher)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Voucher)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=VoucherProxy)
