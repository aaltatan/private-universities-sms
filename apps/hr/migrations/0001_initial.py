# Generated by Django 5.1 on 2025-03-18 23:14

import apps.core.mixins.save
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("edu", "0003_degree_ordering_school_ordering_schoolkind_ordering_and_more"),
        ("geo", "0003_city_ordering_governorate_ordering_and_more"),
        ("org", "0003_costcenter_ordering_group_ordering_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Employee",
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
                    "firstname",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="the field must be at least 2 characters long.",
                            )
                        ],
                        verbose_name="first name",
                    ),
                ),
                (
                    "lastname",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="the field must be at least 2 characters long.",
                            )
                        ],
                        verbose_name="last name",
                    ),
                ),
                (
                    "father_name",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="the field must be at least 2 characters long.",
                            )
                        ],
                        verbose_name="father name",
                    ),
                ),
                (
                    "mother_name",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="the field must be at least 2 characters long.",
                            )
                        ],
                        verbose_name="mother name",
                    ),
                ),
                (
                    "birth_place",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="the field must be at least 2 characters long.",
                            )
                        ],
                        verbose_name="birth place",
                    ),
                ),
                ("birth_date", models.DateField()),
                (
                    "national_id",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="the field must be numeric.", regex="^\\d+$"
                            )
                        ],
                        verbose_name="national id",
                    ),
                ),
                (
                    "passport_id",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="the field must be numeric.", regex="^\\d+$"
                            )
                        ],
                        verbose_name="passport id",
                    ),
                ),
                (
                    "card_id",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="the field must be numeric.", regex="^\\d+$"
                            )
                        ],
                        verbose_name="card id",
                    ),
                ),
                (
                    "civil_registry_office",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="civil registry office",
                    ),
                ),
                (
                    "registry_office_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="registry office name",
                    ),
                ),
                (
                    "registry_office_id",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="the field must be numeric.", regex="^\\d+$"
                            )
                        ],
                        verbose_name="registry office id",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")],
                        default="male",
                        max_length=10,
                    ),
                ),
                (
                    "face_color",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="face color",
                    ),
                ),
                (
                    "eyes_color",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="eyes color",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, default="", max_length=255, verbose_name="address"
                    ),
                ),
                (
                    "special_signs",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="special signs",
                    ),
                ),
                ("card_date", models.DateField(blank=True, null=True)),
                (
                    "martial_status",
                    models.CharField(
                        choices=[
                            ("married", "Married"),
                            ("single", "Single"),
                            ("divorced", "Divorced"),
                            ("other", "Other"),
                        ],
                        default="single",
                        max_length=30,
                    ),
                ),
                (
                    "military_status",
                    models.CharField(
                        choices=[
                            ("defremented", "Defremented"),
                            ("in progress", "In Progress"),
                            ("finished", "Finished"),
                            ("excused", "Excused"),
                            ("other", "Other"),
                        ],
                        default="excused",
                        max_length=30,
                    ),
                ),
                (
                    "religion",
                    models.CharField(
                        choices=[
                            ("muslim", "Muslim"),
                            ("christian", "Christian"),
                            ("jewish", "Jewish"),
                            ("other", "Other"),
                        ],
                        default="muslim",
                        max_length=30,
                    ),
                ),
                (
                    "current_address",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                ("hire_date", models.DateField()),
                (
                    "notes",
                    models.TextField(
                        blank=True, default="", max_length=1000, verbose_name="notes"
                    ),
                ),
                (
                    "profile",
                    models.ImageField(blank=True, null=True, upload_to="profiles"),
                ),
                (
                    "identity_document",
                    models.FileField(blank=True, null=True, upload_to="identities"),
                ),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                    ),
                ),
                ("ordering", models.PositiveIntegerField(default=0)),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="geo.city",
                    ),
                ),
                (
                    "cost_center",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="org.costcenter",
                    ),
                ),
                (
                    "degree",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="edu.degree",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True, related_name="employees", to="org.group"
                    ),
                ),
                (
                    "job_subtype",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="org.jobsubtype",
                    ),
                ),
                (
                    "nationality",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="geo.nationality",
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="org.position",
                    ),
                ),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="edu.school",
                    ),
                ),
                (
                    "specialization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="edu.specialization",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="org.status",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employee",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Employee",
                "verbose_name_plural": "Employees",
                "ordering": ("firstname",),
                "permissions": (
                    ("export_employee", "Can export employee"),
                    ("view_activity_employee", "Can view employee activity"),
                ),
            },
            bases=(apps.core.mixins.save.AddCreateActivityMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Email",
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
                ("email", models.EmailField(max_length=255, verbose_name="email")),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("personal", "Personal"),
                            ("work", "Work"),
                            ("other", "Other"),
                        ],
                        default="personal",
                        max_length=30,
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, default="", max_length=1000, verbose_name="notes"
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="emails",
                        to="hr.employee",
                    ),
                ),
            ],
            bases=(apps.core.mixins.save.AddCreateActivityMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Mobile",
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
                    "number",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="the field must be syrian mobile number like 0947302503.",
                                regex="^09\\d{8}$",
                            )
                        ],
                        verbose_name="mobile number",
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("personal", "Personal"),
                            ("work", "Work"),
                            ("other", "Other"),
                        ],
                        default="personal",
                        max_length=30,
                    ),
                ),
                (
                    "has_whatsapp",
                    models.BooleanField(default=True, verbose_name="has whatsapp"),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, default="", max_length=1000, verbose_name="notes"
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mobiles",
                        to="hr.employee",
                    ),
                ),
            ],
            bases=(apps.core.mixins.save.AddCreateActivityMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Phone",
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
                    "number",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="the field must be syrian phone number like 0332756651.",
                                regex="^0\\d{2}\\d{6,7}$",
                            )
                        ],
                        verbose_name="phone number",
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("personal", "Personal"),
                            ("work", "Work"),
                            ("other", "Other"),
                        ],
                        default="personal",
                        max_length=30,
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, default="", max_length=1000, verbose_name="notes"
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="phones",
                        to="hr.employee",
                    ),
                ),
            ],
            bases=(apps.core.mixins.save.AddCreateActivityMixin, models.Model),
        ),
    ]
