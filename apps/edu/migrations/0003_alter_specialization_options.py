# Generated by Django 5.1 on 2025-02-21 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("edu", "0002_specialization"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="specialization",
            options={
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
    ]
