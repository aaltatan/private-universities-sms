# Generated by Django 5.1 on 2025-08-01 22:29

import apps.core.mixins.save
import apps.core.models.abstracts
import apps.core.validators
import django.core.validators
import django.db.models.deletion
import django.db.models.functions.text
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("edu", "0001_initial"),
        ("geo", "0001_initial"),
        ("org", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HRSetting",
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
                    "min_employee_age",
                    models.PositiveIntegerField(
                        default=18,
                        help_text="allowed min employee age",
                        verbose_name="min employee age",
                    ),
                ),
                (
                    "nth_job_anniversary",
                    models.PositiveIntegerField(
                        default=2,
                        help_text="years count to calculate job anniversary",
                        verbose_name="nth job anniversary",
                    ),
                ),
                (
                    "years_count_to_group_job_age",
                    models.PositiveIntegerField(
                        default=2,
                        help_text="years count to group job age",
                        verbose_name="years count to group job age",
                    ),
                ),
            ],
            options={
                "verbose_name": "Hr Settings",
                "ordering": ("id",),
            },
        ),
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
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
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
                    "fullname",
                    models.GeneratedField(
                        db_persist=False,
                        expression=django.db.models.functions.text.Concat(
                            models.F("firstname"),
                            models.Value(" "),
                            models.F("father_name"),
                            models.Value(" "),
                            models.F("lastname"),
                        ),
                        output_field=models.CharField(max_length=255),
                        verbose_name="full name",
                    ),
                ),
                (
                    "shortname",
                    models.GeneratedField(
                        db_persist=False,
                        expression=django.db.models.functions.text.Concat(
                            models.F("firstname"),
                            models.Value(" "),
                            models.F("lastname"),
                        ),
                        output_field=models.CharField(max_length=255),
                        verbose_name="short name",
                    ),
                ),
                (
                    "father_fullname",
                    models.GeneratedField(
                        db_persist=False,
                        expression=django.db.models.functions.text.Concat(
                            models.F("father_name"),
                            models.Value(" "),
                            models.F("lastname"),
                        ),
                        output_field=models.CharField(max_length=255),
                        verbose_name="father full name",
                    ),
                ),
                (
                    "autocomplete",
                    models.GeneratedField(
                        db_persist=False,
                        expression=django.db.models.functions.text.Concat(
                            models.F("firstname"),
                            models.Value(" "),
                            models.F("father_name"),
                            models.Value(" "),
                            models.F("lastname"),
                            models.Value(" ["),
                            models.F("national_id"),
                            models.Value("]"),
                        ),
                        output_field=models.CharField(max_length=1000),
                        verbose_name="autocomplete for searching",
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
                ("birth_date", models.DateField(verbose_name="birth date")),
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
                        verbose_name="gender",
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
                (
                    "card_date",
                    models.DateField(blank=True, null=True, verbose_name="card date"),
                ),
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
                        verbose_name="martial status",
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
                        verbose_name="military status",
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
                        verbose_name="religion",
                    ),
                ),
                (
                    "current_address",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="current address",
                    ),
                ),
                ("hire_date", models.DateField()),
                (
                    "separation_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="separation date"
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, default="", max_length=1000, verbose_name="notes"
                    ),
                ),
                (
                    "profile",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="profiles",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "jpeg", "png"],
                                message="the field must be a valid jpg, jpeg or png file.",
                            ),
                            apps.core.validators.validate_image_mimetype,
                        ],
                        verbose_name="profile",
                    ),
                ),
                (
                    "identity_document",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="identities",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["pdf", "png", "jpg", "jpeg"],
                                message="the field must be a valid pdf, png, jpg or jpeg file.",
                            ),
                            apps.core.validators.validate_pdf_image_mimetype,
                        ],
                        verbose_name="identity document",
                    ),
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
                        verbose_name="city",
                    ),
                ),
                (
                    "cost_center",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="org.costcenter",
                        verbose_name="cost center",
                    ),
                ),
                (
                    "degree",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="edu.degree",
                        verbose_name="degree",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        related_name="employees",
                        to="org.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "job_subtype",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="org.jobsubtype",
                        verbose_name="job subtype",
                    ),
                ),
                (
                    "nationality",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="geo.nationality",
                        verbose_name="nationality",
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="org.position",
                        verbose_name="position",
                    ),
                ),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="edu.school",
                        verbose_name="school",
                    ),
                ),
                (
                    "specialization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="edu.specialization",
                        verbose_name="specialization",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to="org.status",
                        verbose_name="status",
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
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Employee",
                "verbose_name_plural": "Employees",
                "ordering": (
                    "-status__is_payable",
                    "status__name",
                    "cost_center__name",
                    "job_subtype__name",
                    "specialization__name",
                    "degree__name",
                    "fullname",
                ),
                "permissions": (
                    ("export_employee", "Can export employee"),
                    ("view_activity_employee", "Can view employee activity"),
                ),
            },
            bases=(
                apps.core.models.abstracts.UrlsMixin,
                apps.core.mixins.save.AddCreateActivityMixin,
                models.Model,
            ),
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
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="email"
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
                ("ordering", models.PositiveIntegerField(default=0)),
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
            options={
                "verbose_name": "email",
                "verbose_name_plural": "emails",
                "ordering": ("kind", "email"),
            },
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
                        unique=True,
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
                ("ordering", models.PositiveIntegerField(default=0)),
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
            options={
                "verbose_name": "mobile",
                "verbose_name_plural": "mobiles",
                "ordering": ("kind", "number"),
            },
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
                ("ordering", models.PositiveIntegerField(default=0)),
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
            options={
                "verbose_name": "phone",
                "verbose_name_plural": "phones",
                "ordering": ("kind", "number"),
            },
            bases=(apps.core.mixins.save.AddCreateActivityMixin, models.Model),
        ),
        migrations.AddIndex(
            model_name="employee",
            index=models.Index(
                fields=["firstname", "father_name", "lastname"],
                name="hr_employee_firstna_7af8e7_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="employee",
            index=models.Index(
                fields=["birth_date"], name="hr_employee_birth_d_0b04ff_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="employee",
            index=models.Index(
                fields=["hire_date"], name="hr_employee_hire_da_4d71d0_idx"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="phone",
            unique_together={("employee", "number")},
        ),
    ]
