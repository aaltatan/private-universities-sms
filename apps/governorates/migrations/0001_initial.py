# Generated by Django 5.1 on 2024-12-20 13:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Governorate",
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
                ("description", models.TextField(blank=True, default="", null=True)),
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
                "ordering": ("name",),
                "permissions": (("export_governorate", "Can export governorate"),),
            },
        ),
    ]