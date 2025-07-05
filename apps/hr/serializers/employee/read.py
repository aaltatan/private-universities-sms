from rest_framework import serializers

from apps.core import models as core_models
from apps.edu import models as edu_models
from apps.geo import models as geo_models
from apps.org import models as org_models

from ... import models


class EmployeeSerializer(serializers.ModelSerializer):
    class NationalitySerializer(serializers.ModelSerializer):
        class Meta:
            model = geo_models.Nationality
            fields = ("id", "name", "is_local", "description")

    class CitySerializer(serializers.ModelSerializer):
        class GovernorateSerializer(serializers.ModelSerializer):
            class Meta:
                model = geo_models.Governorate
                fields = ("id", "name", "description")

        governorate = GovernorateSerializer(read_only=True)

        class Meta:
            model = geo_models.City
            fields = ("id", "name", "kind", "governorate", "description")

    class CostCenterSerializer(serializers.ModelSerializer):
        class Meta:
            model = org_models.CostCenter
            fields = ("id", "name", "accounting_id", "description")

    class PositionSerializer(serializers.ModelSerializer):
        class Meta:
            model = org_models.Position
            fields = ("id", "name", "order", "description")

    class StatusSerializer(serializers.ModelSerializer):
        class Meta:
            model = org_models.Status
            fields = ("id", "name", "is_payable", "description")

    class JobSubtypeSerializer(serializers.ModelSerializer):
        class JobTypeSerializer(serializers.ModelSerializer):
            class Meta:
                model = org_models.JobType
                fields = ("id", "name", "description")

        job_type = JobTypeSerializer(read_only=True)

        class Meta:
            model = org_models.JobSubtype
            fields = ("id", "name", "job_type", "description")

    class GroupSerializer(serializers.ModelSerializer):
        class Meta:
            model = org_models.Group
            fields = ("id", "name", "kind", "description")

    class DegreeSerializer(serializers.ModelSerializer):
        class Meta:
            model = edu_models.Degree
            fields = ("id", "name", "order", "is_academic", "description")

    class SchoolSerializer(serializers.ModelSerializer):
        class KindSerializer(serializers.ModelSerializer):
            class Meta:
                model = edu_models.SchoolKind
                fields = ("id", "name", "is_governmental", "is_virtual", "description")

        class NationalitySerializer(serializers.ModelSerializer):
            class Meta:
                model = geo_models.Nationality
                fields = ("id", "name", "is_local", "description")

        kind = KindSerializer(read_only=True)
        nationality = NationalitySerializer(read_only=True)

        class Meta:
            model = edu_models.School
            fields = (
                "id",
                "name",
                "kind",
                "nationality",
                "website",
                "email",
                "phone",
                "address",
                "description",
            )

    class SpecializationSerializer(serializers.ModelSerializer):
        class Meta:
            model = edu_models.Specialization
            fields = ("id", "name", "is_specialist", "description")

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = core_models.User
            fields = ("id", "username", "email", "first_name", "last_name")

    class EmailSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Email
            fields = ("id", "email", "kind", "notes")

    class MobileSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Mobile
            fields = ("id", "number", "kind", "has_whatsapp", "notes")

    class PhoneSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Phone
            fields = ("id", "number", "kind", "notes")

    fullname = serializers.CharField()
    shortname = serializers.CharField()
    father_fullname = serializers.CharField()
    age = serializers.IntegerField()
    age_group = serializers.CharField()
    next_birthday = serializers.DateField()
    nationality = NationalitySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    job_age = serializers.IntegerField()
    job_age_group = serializers.CharField()
    next_job_anniversary = serializers.DateField()
    cost_center = CostCenterSerializer(read_only=True)
    position = PositionSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    job_subtype = JobSubtypeSerializer(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    degree = DegreeSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    specialization = SpecializationSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    mobiles = MobileSerializer(many=True, read_only=True)
    phones = PhoneSerializer(many=True, read_only=True)
    emails = EmailSerializer(many=True, read_only=True)

    class Meta:
        model = models.Employee
        fields = (
            "id",
            "fullname",
            "shortname",
            "firstname",
            "lastname",
            "father_name",
            "father_fullname",
            "mother_name",
            "birth_place",
            "birth_date",
            "age",
            "age_group",
            "next_birthday",
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
            "job_age",
            "job_age_group",
            "next_job_anniversary",
            "notes",
            "profile",
            "identity_document",
            "cost_center",
            "position",
            "status",
            "job_subtype",
            "groups",
            "degree",
            "school",
            "specialization",
            "user",
            "mobiles",
            "phones",
            "emails",
        )
