# Generated by Django 5.1 on 2025-06-06 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fin", "0006_alter_compensation_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="compensation",
            name="max_value",
            field=models.DecimalField(
                decimal_places=4,
                default=500000000,
                max_digits=20,
                verbose_name="max value",
            ),
        ),
        migrations.AddField(
            model_name="compensation",
            name="min_value",
            field=models.DecimalField(
                decimal_places=4, default=0, max_digits=20, verbose_name="min value"
            ),
        ),
    ]
