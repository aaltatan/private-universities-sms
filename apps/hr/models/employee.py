import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Concat
from django.db.models.signals import pre_delete, pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core import signals, validators
from apps.core.mixins import AddCreateActivityMixin
from apps.core.models import User
from apps.core.models.abstracts import UrlsMixin
from apps.core.utils import calculate_age_in_years
from apps.core.validators import (
    numeric_validator,
    two_chars_validator,
)
from apps.edu.models import Degree, School, Specialization
from apps.geo.models import City, Nationality
from apps.org.models import CostCenter, Group, JobSubtype, Position, Status

from ..managers import EmployeeManager
from .setting import HRSetting


class Employee(UrlsMixin, AddCreateActivityMixin, models.Model):
    class ReligionChoices(models.TextChoices):
        MUSLIM = "muslim", _("muslim")
        CHRISTIAN = "christian", _("christian")
        JEWISH = "jewish", _("jewish")
        OTHER = "other", _("other")

    class GenderChoices(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")

    class MartialStatusChoices(models.TextChoices):
        MARRIED = "married", _("married")
        SINGLE = "single", _("single")
        DIVORCED = "divorced", _("divorced")
        OTHER = "other", _("other")

    class MilitaryStatus(models.TextChoices):
        DEFREMENTED = "defremented", _("defremented")
        IN_PROGRESS = "in progress", _("in progress")
        FINISHED = "finished", _("finished")
        EXCUSED = "excused", _("excused")
        OTHER = "other", _("other")

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    firstname = models.CharField(
        max_length=255,
        verbose_name=_("first name"),
        validators=[two_chars_validator],
    )
    lastname = models.CharField(
        max_length=255,
        verbose_name=_("last name"),
        validators=[two_chars_validator],
    )
    father_name = models.CharField(
        max_length=255,
        verbose_name=_("father name"),
        validators=[two_chars_validator],
    )
    fullname = models.GeneratedField(
        expression=Concat(
            models.F("firstname"),
            models.Value(" "),
            models.F("father_name"),
            models.Value(" "),
            models.F("lastname"),
        ),
        verbose_name=_("full name"),
        output_field=models.CharField(max_length=255),
        db_persist=False,
    )
    shortname = models.GeneratedField(
        expression=Concat(
            models.F("firstname"),
            models.Value(" "),
            models.F("lastname"),
        ),
        verbose_name=_("short name"),
        output_field=models.CharField(max_length=255),
        db_persist=False,
    )
    father_fullname = models.GeneratedField(
        expression=Concat(
            models.F("father_name"),
            models.Value(" "),
            models.F("lastname"),
        ),
        verbose_name=_("father full name"),
        output_field=models.CharField(max_length=255),
        db_persist=False,
    )
    autocomplete = models.GeneratedField(
        expression=Concat(
            models.F("firstname"),
            models.Value(" "),
            models.F("father_name"),
            models.Value(" "),
            models.F("lastname"),
            models.Value(" ["),
            models.F("national_id"),
            models.Value("]"),
        ),
        verbose_name=_("autocomplete for searching"),
        output_field=models.CharField(max_length=1000),
        db_persist=False,
    )
    mother_name = models.CharField(
        max_length=255,
        verbose_name=_("mother name"),
        validators=[two_chars_validator],
    )
    birth_place = models.CharField(
        max_length=255,
        verbose_name=_("birth place"),
        validators=[two_chars_validator],
    )
    birth_date = models.DateField(
        verbose_name=_("birth date"),
    )
    national_id = models.CharField(
        max_length=255,
        verbose_name=_("national id"),
        unique=True,
        validators=[numeric_validator],
    )
    passport_id = models.CharField(
        max_length=255,
        verbose_name=_("passport id"),
        unique=True,
        null=True,
        blank=True,
        validators=[numeric_validator],
    )
    card_id = models.CharField(
        max_length=255,
        verbose_name=_("card id"),
        unique=True,
        null=True,
        blank=True,
        validators=[numeric_validator],
    )
    # أمانة السجل المدني
    civil_registry_office = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name=_("civil registry office"),
    )
    # قيد السجل المدني
    registry_office_name = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name=_("registry office name"),
    )
    # رقم السجل المدني
    registry_office_id = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name=_("registry office id"),
        validators=[numeric_validator],
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE,
        verbose_name=_("gender"),
    )
    face_color = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name=_("face color"),
    )
    eyes_color = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name=_("eyes color"),
    )
    address = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name=_("address"),
    )
    special_signs = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name=_("special signs"),
    )
    card_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("card date"),
    )
    martial_status = models.CharField(
        max_length=30,
        choices=MartialStatusChoices.choices,
        default=MartialStatusChoices.SINGLE,
        verbose_name=_("martial status"),
    )
    military_status = models.CharField(
        max_length=30,
        choices=MilitaryStatus.choices,
        default=MilitaryStatus.EXCUSED,
        verbose_name=_("military status"),
    )
    religion = models.CharField(
        max_length=30,
        choices=ReligionChoices.choices,
        default=ReligionChoices.MUSLIM,
        verbose_name=_("religion"),
    )
    current_address = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name=_("current address"),
    )
    # geo
    nationality = models.ForeignKey(
        Nationality,
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("nationality"),
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("city"),
    )
    hire_date = models.DateField(
        verbose_name=_("hire date"),
    )
    separation_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("separation date"),
    )
    notes = models.TextField(
        verbose_name=_("notes"),
        max_length=1000,
        default="",
        blank=True,
    )
    profile = models.ImageField(
        upload_to="profiles",
        null=True,
        blank=True,
        verbose_name=_("profile"),
        validators=[
            validators.image_extension_validator,
            validators.validate_image_mimetype,
        ],
    )
    identity_document = models.FileField(
        upload_to="identities",
        null=True,
        blank=True,
        verbose_name=_("identity document"),
        validators=[
            validators.pdf_image_extension_validator,
            validators.validate_pdf_image_mimetype,
        ],
    )
    # org
    cost_center = models.ForeignKey(
        CostCenter,
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("cost center"),
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("position"),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("status"),
    )
    job_subtype = models.ForeignKey(
        JobSubtype,
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("job subtype"),
    )
    groups = models.ManyToManyField(
        Group,
        related_name="employees",
        blank=True,
        verbose_name=_("groups"),
    )
    # edu
    degree = models.ForeignKey(
        Degree,
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("degree"),
    )
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("school"),
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("specialization"),
    )
    # user
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="employee",
        null=True,
        blank=True,
        verbose_name=_("user"),
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        null=True,
        blank=True,
        allow_unicode=True,
    )
    ordering = models.PositiveIntegerField(
        default=0,
    )  # to order objects in inlines

    objects: EmployeeManager = EmployeeManager()

    class Meta:
        ordering = (
            "-status__is_payable",
            "status__name",
            "cost_center__name",
            "job_subtype__name",
            "specialization__name",
            "degree__name",
            "fullname",
        )
        icon = "user"
        codename_plural = "employees"
        verbose_name = _("employee")
        verbose_name_plural = _("employees")
        permissions = (
            ("export_employee", "Can export employee"),
            ("view_activity_employee", "Can view employee activity"),
        )
        indexes = [
            models.Index(fields=["firstname", "father_name", "lastname"]),
            models.Index(fields=["birth_date"]),
            models.Index(fields=["hire_date"]),
        ]

    def clean(self):
        errors: dict[str, ValidationError] = {}

        # birth date
        if timezone.now().date() < self.birth_date:
            errors["birth_date"] = ValidationError(
                _("birth date cannot be in the future"),
            )

        min_age = HRSetting.get_solo().min_employee_age
        age = calculate_age_in_years(self.birth_date)

        if age < min_age:
            errors["birth_date"] = ValidationError(
                _("employee's age must be at least {} years old").format(min_age),
            )

        # hire date
        if timezone.now().date() < self.hire_date:
            errors["hire_date"] = ValidationError(
                _("hire date cannot be in the future"),
            )

        if self.hire_date < self.birth_date:
            errors["hire_date"] = ValidationError(
                _("hire date cannot be earlier than birth date"),
            )

        # card date
        if self.card_date:
            if timezone.now().date() < self.card_date:
                errors["card_date"] = ValidationError(
                    _("card date cannot be in the future"),
                )

            if self.card_date < self.birth_date:
                errors["card_date"] = ValidationError(
                    _("card date cannot be earlier than birth date"),
                )

        # separation date
        if self.status.is_separated and self.separation_date is None:
            errors["separation_date"] = ValidationError(
                _(
                    "separation date cannot be empty if the employee status is separated"
                ),
            )

        if self.separation_date and not self.status.is_separated:
            errors["separation_date"] = ValidationError(
                _(
                    "separation date cannot be filled if the employee status is not separated"
                ),
            )

        if self.separation_date and self.separation_date < self.hire_date:
            errors["separation_date"] = ValidationError(
                _("separation date cannot be earlier than hire date"),
            )

        if errors:
            raise ValidationError(errors)

    def get_fullname(self) -> str:
        return f"{self.firstname} {self.father_name} {self.lastname}"

    def get_age(self) -> int:
        return calculate_age_in_years(self.birth_date)

    def get_job_age(self) -> int:
        if self.separation_date:
            return calculate_age_in_years(self.hire_date, self.separation_date)

        return calculate_age_in_years(self.hire_date)

    def get_next_birthday(self):
        return timezone.datetime(
            timezone.now().year, self.birth_date.month, self.birth_date.day
        ).date()

    def get_ledger_url(self):
        return reverse("reports:ledger:index", kwargs={"slug": self.slug})

    def get_ledger_msword_url(self):
        return reverse("reports:ledger:msword", kwargs={"slug": self.slug})

    def get_word_url(self):
        return reverse("hr:employees:word", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return f"{self.get_fullname()} - {self.cost_center.name} [{self.national_id}]"


def employee_pre_save(sender, instance: Employee, *args, **kwargs):
    instance.slug = slugify(
        f"{instance.get_fullname()}-{instance.national_id}", allow_unicode=True
    )

    if instance.gender == instance.GenderChoices.FEMALE.value:
        instance.military_status = instance.MilitaryStatus.EXCUSED.value


def employee_post_delete(sender, instance: Employee, *args, **kwargs):
    instance.profile.delete()
    instance.identity_document.delete()


class ActivitySerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="city.name")
    nationality = serializers.CharField(source="nationality.name")
    cost_center = serializers.CharField(source="cost_center.name")
    position = serializers.CharField(source="position.name")
    status = serializers.CharField(source="status.name")
    job_subtype = serializers.CharField(source="job_subtype.name")
    degree = serializers.CharField(source="degree.name")
    school = serializers.CharField(source="school.name")
    specialization = serializers.CharField(source="specialization.name")
    username = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    def get_username(self, obj: Employee) -> str:
        return obj.user.username if obj.user else ""

    def get_groups(self, obj: Employee) -> str:
        return ", ".join([group.name for group in obj.groups.all()])

    class Meta:
        model = Employee
        fields = (
            "firstname",
            "lastname",
            "father_name",
            "mother_name",
            "birth_place",
            "birth_date",
            "national_id",
            "passport_id",
            "card_id",
            "civil_registry_office",
            "registry_office_name",
            "registry_office_id",
            "gender",
            "face_color",
            "eyes_color",
            "address",
            "special_signs",
            "card_date",
            "martial_status",
            "military_status",
            "religion",
            "current_address",
            "nationality",
            "city",
            "hire_date",
            "separation_date",
            "notes",
            "cost_center",
            "position",
            "status",
            "job_subtype",
            "degree",
            "school",
            "specialization",
            "username",
            "groups",
        )


pre_save.connect(employee_pre_save, Employee)
pre_delete.connect(employee_post_delete, Employee)
pre_save.connect(signals.add_update_activity(ActivitySerializer), sender=Employee)
pre_delete.connect(signals.add_delete_activity(ActivitySerializer), sender=Employee)
