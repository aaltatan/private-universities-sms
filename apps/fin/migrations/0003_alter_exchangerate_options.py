# Generated by Django 5.1 on 2025-04-04 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("fin", "0002_alter_currency_code_alter_currency_decimal_places_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exchangerate",
            options={
                "ordering": ("-currency__is_primary", "created_at", "date"),
                "permissions": (
                    ("export_exchangerate", "Can export exchange rate"),
                    ("view_activity_exchangerate", "Can view exchange rate activity"),
                ),
                "verbose_name": "Exchange Rate",
                "verbose_name_plural": "Exchange Rates",
            },
        ),
    ]
