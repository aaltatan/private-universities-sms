# Generated by Django 5.1 on 2025-03-04 21:02

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("geo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Degree",
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
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
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
                        default=1, help_text="order of degree", verbose_name="order"
                    ),
                ),
                (
                    "is_academic",
                    models.BooleanField(
                        default=True,
                        help_text="is an academic degree",
                        verbose_name="is academic",
                    ),
                ),
            ],
            options={
                "verbose_name": "Degree",
                "verbose_name_plural": "Degrees",
                "ordering": ("-is_academic", "order", "name"),
                "permissions": (
                    ("export_degree", "Can export degree"),
                    ("view_activity_degree", "Can view degree activity"),
                ),
            },
        ),
        migrations.CreateModel(
            name="SchoolKind",
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
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
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
                    "is_governmental",
                    models.BooleanField(
                        default=True,
                        help_text="is it governmental or private",
                        verbose_name="is governmental",
                    ),
                ),
                (
                    "is_virtual",
                    models.BooleanField(
                        default=False,
                        help_text="is it virtual or ordinary",
                        verbose_name="is virtual",
                    ),
                ),
            ],
            options={
                "verbose_name": "School Kind",
                "verbose_name_plural": "School Kinds",
                "ordering": ("name",),
                "permissions": (
                    ("export_schoolkind", "Can export school kind"),
                    ("view_activity_schoolkind", "Can view school kind activity"),
                ),
            },
        ),
        migrations.CreateModel(
            name="Specialization",
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
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
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
                    "is_specialist",
                    models.BooleanField(
                        default=True,
                        help_text="is a specialist or supporter",
                        verbose_name="is specialist",
                    ),
                ),
            ],
            options={
                "verbose_name": "Specialization",
                "verbose_name_plural": "Specializations",
                "ordering": ("-is_specialist", "name"),
                "permissions": (
                    ("export_specialization", "Can export specialization"),
                    (
                        "view_activity_specialization",
                        "Can view specialization activity",
                    ),
                ),
            },
        ),
        migrations.CreateModel(
            name="School",
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
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="description"
                    ),
                ),
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
                    "website",
                    models.URLField(
                        blank=True,
                        default="",
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="website",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        default="",
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="email",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        null=True,
                        verbose_name="phone",
                    ),
                ),
                (
                    "nationality",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="schools",
                        to="geo.nationality",
                        verbose_name="nationality",
                    ),
                ),
                (
                    "kind",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="schools",
                        to="edu.schoolkind",
                        verbose_name="kind",
                    ),
                ),
            ],
            options={
                "verbose_name": "School",
                "verbose_name_plural": "Schools",
                "ordering": ("name",),
                "permissions": (
                    ("export_school", "Can export school"),
                    ("view_activity_school", "Can view school activity"),
                ),
            },
        ),
    ]
