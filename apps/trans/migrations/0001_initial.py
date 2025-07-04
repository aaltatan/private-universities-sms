# Generated by Django 5.1 on 2025-06-21 19:52

import apps.core.mixins.save
import apps.core.models.abstracts
import apps.core.validators
import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("fin", "0012_compensation_shortname"),
        ("hr", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Voucher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "voucher_serial",
                    models.CharField(
                        editable=False,
                        max_length=20,
                        unique=True,
                        verbose_name="voucher serial",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                ("date", models.DateField(verbose_name="date")),
                (
                    "month",
                    models.CharField(
                        choices=[
                            ("january", "January"),
                            ("february", "February"),
                            ("march", "March"),
                            ("april", "April"),
                            ("may", "May"),
                            ("june", "June"),
                            ("july", "July"),
                            ("august", "August"),
                            ("september", "September"),
                            ("october", "October"),
                            ("november", "November"),
                            ("december", "December"),
                        ],
                        default="january",
                        max_length=255,
                        verbose_name="month",
                    ),
                ),
                (
                    "quarter",
                    models.CharField(
                        choices=[
                            ("q1", "First Quarter"),
                            ("q2", "Second Quarter"),
                            ("q3", "Third Quarter"),
                            ("q4", "Fourth Quarter"),
                        ],
                        default="q1",
                        max_length=255,
                        verbose_name="quarter",
                    ),
                ),
                (
                    "notes",
                    models.TextField(blank=True, default="", verbose_name="notes"),
                ),
                (
                    "serial_id",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="dewan id if exists",
                        max_length=255,
                        verbose_name="serial id",
                    ),
                ),
                (
                    "serial_date",
                    models.DateField(
                        blank=True,
                        help_text="dewan date if exists",
                        null=True,
                        verbose_name="serial date",
                    ),
                ),
                (
                    "approve_date",
                    models.DateField(
                        blank=True,
                        help_text="date of approve by vouchers orderer (signature)",
                        null=True,
                        verbose_name="approve date",
                    ),
                ),
                (
                    "due_date",
                    models.DateField(blank=True, null=True, verbose_name="due date"),
                ),
                (
                    "document",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="vouchers",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["pdf", "png", "jpg", "jpeg"],
                                message="the field must be a valid pdf, png, jpg or jpeg file.",
                            ),
                            apps.core.validators.validate_pdf_image_mimetype,
                        ],
                        verbose_name="document",
                    ),
                ),
                (
                    "accounting_journal_sequence",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="the sequence of the accounting journal in accounting system e.g. JOV0001",
                        max_length=255,
                        verbose_name="accounting journal sequence",
                    ),
                ),
                (
                    "is_audited",
                    models.BooleanField(default=False, verbose_name="is audited"),
                ),
                (
                    "is_migrated",
                    models.BooleanField(default=False, verbose_name="is migrated"),
                ),
                (
                    "audited_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="audited_vouchers",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="audited by",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vouchers",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
                (
                    "kind",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vouchers",
                        to="fin.voucherkind",
                        verbose_name="kind",
                    ),
                ),
                (
                    "period",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vouchers",
                        to="fin.period",
                        verbose_name="period",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="updated_vouchers",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Voucher",
                "verbose_name_plural": "Vouchers",
                "ordering": ("-date", "-created_at", "voucher_serial"),
                "permissions": (
                    ("export_voucher", "Can export voucher"),
                    ("migrate_voucher", "Can migrate voucher"),
                    ("unmigrate_voucher", "Can unmigrate voucher"),
                    ("audit_voucher", "Can audit voucher"),
                    ("unaudit_voucher", "Can unaudit voucher"),
                    ("view_activity_voucher", "Can view voucher activity"),
                ),
            },
            bases=(
                apps.core.models.abstracts.UrlsMixin,
                apps.core.mixins.save.AddCreateActivityMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="VoucherProxy",
            fields=[],
            options={
                "verbose_name": "voucher proxy",
                "verbose_name_plural": "all vouchers",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("trans.voucher",),
        ),
        migrations.CreateModel(
            name="VoucherTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "quantity",
                    models.DecimalField(
                        decimal_places=4,
                        default=1,
                        max_digits=20,
                        verbose_name="quantity",
                    ),
                ),
                (
                    "value",
                    models.DecimalField(
                        decimal_places=4, default=0, max_digits=20, verbose_name="value"
                    ),
                ),
                (
                    "tax",
                    models.DecimalField(
                        decimal_places=4, default=0, max_digits=20, verbose_name="tax"
                    ),
                ),
                (
                    "notes",
                    models.TextField(blank=True, default="", verbose_name="notes"),
                ),
                ("ordering", models.PositiveIntegerField(default=0)),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "compensation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="fin.compensation",
                        verbose_name="compensation",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="transactions",
                        to="hr.employee",
                        verbose_name="employee",
                    ),
                ),
                (
                    "voucher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="transactions",
                        to="trans.voucher",
                        verbose_name="voucher",
                    ),
                ),
            ],
            options={
                "verbose_name": "Voucher Transaction",
                "verbose_name_plural": "Voucher Transactions",
                "ordering": ("-voucher__date", "voucher__voucher_serial", "ordering"),
                "permissions": (
                    ("export_vouchertransaction", "Can export voucher transaction"),
                    (
                        "view_activity_vouchertransaction",
                        "Can view voucher transaction activity",
                    ),
                ),
            },
            bases=(apps.core.models.abstracts.UrlsMixin, models.Model),
        ),
    ]
