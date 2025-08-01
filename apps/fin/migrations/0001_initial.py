# Generated by Django 5.1 on 2025-08-01 22:29

import apps.core.mixins.save
import apps.core.models.abstracts
import apps.core.validators
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tax",
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
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=4,
                                message="the field must be at least 4 characters long.",
                            )
                        ],
                        verbose_name="name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                ("ordering", models.PositiveIntegerField(default=0)),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "shortname",
                    models.CharField(
                        help_text="to use it in services like sms, whatsapp, etc.",
                        max_length=255,
                        verbose_name="short name",
                    ),
                ),
                (
                    "calculation_method",
                    models.CharField(
                        choices=[
                            ("fixed_amount", "Fixed Amount"),
                            ("fixed_percentage", "Fixed Percentage"),
                            ("brackets", "Brackets"),
                            ("formula", "Formula"),
                        ],
                        default="fixed_amount",
                        max_length=30,
                        verbose_name="calculation method",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=4,
                        default=0,
                        help_text="if you choose fixed amount, this field will be used",
                        max_digits=20,
                        verbose_name="amount",
                    ),
                ),
                (
                    "percentage",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="if you choose fixed percentage, this field will be used",
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1),
                        ],
                        verbose_name="percentage",
                    ),
                ),
                (
                    "formula",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="\n        <strong>Formula to calculate tax value</strong>\n        <ul>\n            <li>- It should be a valid python expression</li>\n            <li>- It should return a decimal number</li>\n            <li>- You can use (compensation, employee and quantity) objects to calculate the value if based on any one of them</li>\n            <li>- You can use underscores (_) to separate numbers as thousands</li>\n        </ul>\n        ",
                        verbose_name="formula",
                    ),
                ),
                (
                    "rounded_to",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="rounded to",
                    ),
                ),
                (
                    "round_method",
                    models.CharField(
                        choices=[
                            ("round", "Normal"),
                            ("floor", "Down"),
                            ("ceil", "Up"),
                        ],
                        default="ceil",
                        max_length=10,
                        verbose_name="round method",
                    ),
                ),
                (
                    "affected_by_working_days",
                    models.BooleanField(
                        default=False, verbose_name="affected by working days"
                    ),
                ),
                (
                    "accounting_id",
                    models.CharField(
                        blank=True,
                        default="31",
                        help_text="accounting id in accounting system (in chart of accounts)",
                        max_length=15,
                        null=True,
                        verbose_name="accounting id",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tax",
                "verbose_name_plural": "Taxes",
                "ordering": ("calculation_method", "name"),
                "permissions": (
                    ("export_tax", "Can export tax"),
                    ("view_activity_tax", "Can view tax activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="VoucherKind",
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
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=4,
                                message="the field must be at least 4 characters long.",
                            )
                        ],
                        verbose_name="name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                ("ordering", models.PositiveIntegerField(default=0)),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Voucher Kind",
                "verbose_name_plural": "Voucher Kinds",
                "ordering": ("name",),
                "permissions": (
                    ("export_voucherkind", "Can export voucher kind"),
                    ("view_activity_voucherkind", "Can view voucher kind activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Year",
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
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=4,
                                message="the field must be at least 4 characters long.",
                            )
                        ],
                        verbose_name="name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                ("ordering", models.PositiveIntegerField(default=0)),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Year",
                "verbose_name_plural": "Years",
                "ordering": ("name",),
                "permissions": (
                    ("export_year", "Can export year"),
                    ("view_activity_year", "Can view year activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Compensation",
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
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=4,
                                message="the field must be at least 4 characters long.",
                            )
                        ],
                        verbose_name="name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                ("ordering", models.PositiveIntegerField(default=0)),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "shortname",
                    models.CharField(
                        help_text="to use it in services like sms, whatsapp, etc.",
                        max_length=255,
                        verbose_name="short name",
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[("benefit", "Benefit"), ("cut", "Cut")],
                        default="benefit",
                        max_length=10,
                        verbose_name="kind",
                    ),
                ),
                (
                    "calculation_method",
                    models.CharField(
                        choices=[
                            ("fixed", "Fixed"),
                            ("by_input", "By Input"),
                            ("formula", "Formula"),
                        ],
                        default="by_input",
                        max_length=10,
                        verbose_name="calculation method",
                    ),
                ),
                (
                    "tax_classification",
                    models.CharField(
                        choices=[
                            ("salary", "Salary"),
                            (
                                "withholding_tax_applicable",
                                "Withholding Tax Applicable",
                            ),
                            (
                                "withholding_tax_not_applicable",
                                "Withholding Tax Not Applicable",
                            ),
                            ("others", "Others"),
                        ],
                        default="withholding_tax_applicable",
                        help_text="classify the nature of compensation to know how to calculate it in the periodic tax statement",
                        max_length=255,
                        verbose_name="tax classification",
                    ),
                ),
                (
                    "round_method",
                    models.CharField(
                        choices=[
                            ("round", "Normal"),
                            ("floor", "Down"),
                            ("ceil", "Up"),
                        ],
                        default="ceil",
                        max_length=10,
                        verbose_name="round method",
                    ),
                ),
                (
                    "rounded_to",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="rounded to",
                    ),
                ),
                (
                    "value",
                    models.DecimalField(
                        decimal_places=4, default=0, max_digits=20, verbose_name="value"
                    ),
                ),
                (
                    "min_value",
                    models.DecimalField(
                        decimal_places=4,
                        default=0,
                        max_digits=20,
                        verbose_name="min value",
                    ),
                ),
                (
                    "max_value",
                    models.DecimalField(
                        decimal_places=4,
                        default=500000000,
                        max_digits=20,
                        verbose_name="max value",
                    ),
                ),
                (
                    "affected_by_working_days",
                    models.BooleanField(
                        default=False, verbose_name="affected by working days"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is active"),
                ),
                (
                    "formula",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="\n        <strong>Formula to calculate compensation value</strong>\n        <ul>\n            <li>- It should be a valid python expression</li>\n            <li>- It should return a decimal number</li>\n            <li>- You can use (compensation, employee and quantity) objects to calculate the value if based on any one of them</li>\n            <li>- You can use underscores (_) to separate numbers as thousands</li>\n        </ul>\n        ",
                        verbose_name="formula",
                    ),
                ),
                (
                    "document",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="compensations",
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
                    "accounting_id",
                    models.CharField(
                        blank=True,
                        default="31",
                        help_text="accounting id in accounting system (in chart of accounts)",
                        max_length=15,
                        null=True,
                        verbose_name="accounting id",
                    ),
                ),
                (
                    "tax",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="compensations",
                        to="fin.tax",
                        verbose_name="tax",
                    ),
                ),
            ],
            options={
                "verbose_name": "Compensation",
                "verbose_name_plural": "Compensations",
                "ordering": ("-is_active", "tax__name", "calculation_method", "name"),
                "permissions": (
                    ("export_compensation", "Can export compensation"),
                    ("view_activity_compensation", "Can view compensation activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="TaxBracket",
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
                (
                    "amount_from",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=20,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="amount from",
                    ),
                ),
                (
                    "amount_to",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=20,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="amount to",
                    ),
                ),
                (
                    "rate",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1),
                        ],
                        verbose_name="rate",
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
                        default=None,
                        max_length=255,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "tax",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="brackets",
                        to="fin.tax",
                        verbose_name="tax",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tax Bracket",
                "verbose_name_plural": "Tax Brackets",
                "ordering": ("tax", "amount_from", "amount_to"),
                "permissions": (
                    ("export_taxbracket", "Can export tax bracket"),
                    ("view_activity_taxbracket", "Can view tax bracket activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Period",
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
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=4,
                                message="the field must be at least 4 characters long.",
                            )
                        ],
                        verbose_name="name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
                ("ordering", models.PositiveIntegerField(default=0)),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        unique=True,
                    ),
                ),
                ("start_date", models.DateField(verbose_name="start date")),
                (
                    "is_closed",
                    models.BooleanField(default=False, verbose_name="is closed"),
                ),
                (
                    "year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="periods",
                        to="fin.year",
                        verbose_name="year",
                    ),
                ),
            ],
            options={
                "verbose_name": "Period",
                "verbose_name_plural": "Periods",
                "ordering": ("start_date",),
                "permissions": (
                    ("export_period", "Can export period"),
                    ("view_activity_period", "Can view period activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
    ]
