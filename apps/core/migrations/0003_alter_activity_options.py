# Generated by Django 5.1 on 2025-03-04 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_activity"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="activity",
            options={
                "ordering": ["-created_at", "kind"],
                "verbose_name": "activity",
                "verbose_name_plural": "activities",
            },
        ),
    ]
