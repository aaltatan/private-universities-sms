# Generated by Django 5.1 on 2025-01-20 10:39

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("governorates", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="City",
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
                (
                    "governorate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="cities",
                        to="governorates.governorate",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "cities",
                "ordering": ("name",),
                "permissions": (("export_city", "Can export city"),),
            },
        ),
    ]
