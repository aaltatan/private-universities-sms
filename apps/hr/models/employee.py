from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core import signals
from apps.core.mixins import AddCreateActivityMixin
from apps.core.validators import (
    numeric_validator,
    two_chars_validator,
)
from apps.core.models import User
from apps.edu.models import Degree, School, Specialization
from apps.geo.models import City, Nationality
from apps.org.models import CostCenter, Group, JobSubtype, Position, Status

from ..managers import EmployeeManager


class Employee(AddCreateActivityMixin, models.Model):
    class ReligionChoices(models.TextChoices):
        MUSLIM = "muslim", _("muslim").title()
        CHRISTIAN = "christian", _("christian").title()
        JEWISH = "jewish", _("jewish").title()
        OTHER = "other", _("other").title()

    class GenderChoices(models.TextChoices):
        MALE = "male", _("male").title()
        FEMALE = "female", _("female").title()

    class MartialStatusChoices(models.TextChoices):
        MARRIED = "married", _("married").title()
        SINGLE = "single", _("single").title()
        DIVORCED = "divorced", _("divorced").title()
        OTHER = "other", _("other").title()

    class MilitaryStatus(models.TextChoices):
        DEFREMENTED = "defremented", _("defremented").title()
        IN_PROGRESS = "in progress", _("in progress").title()
        FINISHED = "finished", _("finished").title()
        EXCUSED = "excused", _("excused").title()
        OTHER = "other", _("other").title()

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
    hire_date = models.DateField()
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
    )
    identity_document = models.FileField(
        upload_to="identities",
        null=True,
        blank=True,
        verbose_name=_("identity document"),
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
        ordering = ("firstname",)
        icon = "user"
        codename_plural = "employees"
        verbose_name = _("employee").title()
        verbose_name_plural = _("employees").title()
        permissions = (
            ("export_employee", "Can export employee"),
            ("view_activity_employee", "Can view employee activity"),
        )

    def get_fullname(self) -> str:
        return f"{self.firstname} {self.father_name} {self.lastname}"
    
    def get_shortname(self) -> str:
        return f"{self.firstname} {self.lastname}"

    def __str__(self) -> str:
        return self.get_fullname()

    def get_activities_url(self) -> str:
        app_label: str = self.__get_app_label()
        model_name: str = self.__get_model_name()

        base_url = reverse("core:activities", kwargs={"object_id": self.pk})

        return f"{base_url}?app_label={app_label}&model={model_name}"

    def get_absolute_url(self) -> str:
        verbose_name_plural: str = self.__get_verbose_name_plural()
        return reverse(
            f"{verbose_name_plural}:details",
            kwargs={"slug": self.slug},
        )

    def get_delete_url(self) -> str:
        verbose_name_plural: str = self.__get_verbose_name_plural()
        return reverse(
            f"{verbose_name_plural}:delete",
            kwargs={"slug": self.slug},
        )

    def get_update_url(self) -> str:
        verbose_name_plural: str = self.__get_verbose_name_plural()
        return reverse(
            f"{verbose_name_plural}:update",
            kwargs={"slug": self.slug},
        )

    def __get_verbose_name_plural(self) -> str:
        return self._meta.codename_plural

    def __get_app_label(self) -> str:
        return self._meta.app_label

    def __get_model_name(self) -> str:
        return self._meta.model_name


def employee_pre_save(sender, instance: Employee, *args, **kwargs):
    value = (
        instance.firstname
        + " "
        + instance.father_name
        + " "
        + instance.lastname
        + "-"
        + instance.national_id
    )
    instance.slug = slugify(value, allow_unicode=True)

    if instance.gender == instance.GenderChoices.FEMALE.value:
        instance.military_status = instance.MilitaryStatus.EXCUSED.value


def employee_post_delete(sender, instance: Employee, *args, **kwargs):
    instance.profile.delete()


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
