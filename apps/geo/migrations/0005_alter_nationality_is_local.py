# Generated by Django 5.1 on 2025-06-06 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0004_alter_city_governorate_alter_city_kind_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nationality",
            name="is_local",
            field=models.BooleanField(default=False, verbose_name="is local"),
        ),
    ]
