# Generated by Django 5.1 on 2025-08-01 22:29

import apps.core.mixins.save
import apps.core.models.abstracts
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CostCenter",
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
                    "accounting_id",
                    models.CharField(
                        help_text="cost center id in accounting system",
                        max_length=10,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="the field must be numeric.", regex="^\\d+$"
                            )
                        ],
                        verbose_name="cost center id",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cost Center",
                "verbose_name_plural": "Cost Centers",
                "ordering": ("accounting_id", "name"),
                "permissions": (
                    ("export_costcenter", "Can export cost center"),
                    ("view_activity_costcenter", "Can view cost center activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Group",
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
                    "kind",
                    models.CharField(
                        choices=[
                            ("academic", "Academic"),
                            ("administrative", "Administrative"),
                        ],
                        default="administrative",
                        max_length=50,
                        verbose_name="kind",
                    ),
                ),
            ],
            options={
                "verbose_name": "Group",
                "verbose_name_plural": "Groups",
                "ordering": ("kind", "name"),
                "permissions": (
                    ("export_group", "Can export group"),
                    ("view_activity_group", "Can view group activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="JobType",
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
                "verbose_name": "Job Type",
                "verbose_name_plural": "Job Types",
                "ordering": ("name",),
                "permissions": (
                    ("export_jobtype", "Can export job_type"),
                    ("view_activity_jobtype", "Can view job_type activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Position",
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
                    "order",
                    models.IntegerField(
                        default=1,
                        help_text="for sorting purposes, you can use the same order for different positions",
                        verbose_name="order",
                    ),
                ),
            ],
            options={
                "verbose_name": "Position",
                "verbose_name_plural": "Positions",
                "ordering": ("order", "name"),
                "permissions": (
                    ("export_position", "Can export position"),
                    ("view_activity_position", "Can view position activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Status",
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
                    "is_payable",
                    models.BooleanField(default=True, verbose_name="is payable"),
                ),
                (
                    "is_separated",
                    models.BooleanField(default=False, verbose_name="is separated"),
                ),
            ],
            options={
                "verbose_name": "Status",
                "verbose_name_plural": "Statuses",
                "ordering": ("is_payable", "name"),
                "permissions": (
                    ("export_status", "Can export status"),
                    ("view_activity_status", "Can view status activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="JobSubtype",
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
                    "job_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="job_subtypes",
                        to="org.jobtype",
                        verbose_name="job type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Job Subtype",
                "verbose_name_plural": "Job Subtypes",
                "ordering": ("job_type__name", "name"),
                "permissions": (
                    ("export_jobsubtype", "Can export job_subtype"),
                    ("view_activity_jobsubtype", "Can view job_subtype activity"),
                ),
            },
            bases=(
                apps.core.mixins.save.AddCreateActivityMixin,
                apps.core.models.abstracts.UrlsMixin,
                models.Model,
            ),
        ),
    ]
