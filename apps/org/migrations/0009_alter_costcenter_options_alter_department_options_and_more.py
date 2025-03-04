# Generated by Django 5.1 on 2025-03-04 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("org", "0008_alter_department_cost_center"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="costcenter",
            options={
                "ordering": ("accounting_id", "name"),
                "permissions": (
                    ("export_costcenter", "Can export cost center"),
                    ("view_activity_costcenter", "Can view cost center activity"),
                ),
                "verbose_name": "Cost Center",
                "verbose_name_plural": "Cost Centers",
            },
        ),
        migrations.AlterModelOptions(
            name="department",
            options={
                "ordering": ("name",),
                "permissions": (
                    ("export_department", "Can export department"),
                    ("view_activity_department", "Can view department activity"),
                ),
                "verbose_name": "Department",
                "verbose_name_plural": "Departments",
            },
        ),
        migrations.AlterModelOptions(
            name="group",
            options={
                "ordering": ("name",),
                "permissions": (
                    ("export_group", "Can export group"),
                    ("view_activity_group", "Can view group activity"),
                ),
                "verbose_name": "Group",
                "verbose_name_plural": "Groups",
            },
        ),
        migrations.AlterModelOptions(
            name="jobsubtype",
            options={
                "ordering": ("job_type__name", "name"),
                "permissions": (
                    ("export_jobsubtype", "Can export job_subtype"),
                    ("view_activity_jobsubtype", "Can view job_subtype activity"),
                ),
                "verbose_name": "Job Subtype",
                "verbose_name_plural": "Job Subtypes",
            },
        ),
        migrations.AlterModelOptions(
            name="jobtype",
            options={
                "ordering": ("name",),
                "permissions": (
                    ("export_jobtype", "Can export job_type"),
                    ("view_activity_jobtype", "Can view job_type activity"),
                ),
                "verbose_name": "Job Type",
                "verbose_name_plural": "Job Types",
            },
        ),
        migrations.AlterModelOptions(
            name="position",
            options={
                "ordering": ("order", "name"),
                "permissions": (
                    ("export_position", "Can export position"),
                    ("view_activity_position", "Can view position activity"),
                ),
                "verbose_name": "Position",
                "verbose_name_plural": "Positions",
            },
        ),
        migrations.AlterModelOptions(
            name="status",
            options={
                "ordering": ("is_payable", "name"),
                "permissions": (
                    ("export_status", "Can export status"),
                    ("view_activity_status", "Can view status activity"),
                ),
                "verbose_name": "Status",
                "verbose_name_plural": "Statuses",
            },
        ),
    ]
