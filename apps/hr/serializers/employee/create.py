from rest_framework import serializers

from apps.core import models as core_models
from apps.edu import models as edu_models
from apps.geo import models as geo_models
from apps.org import models as org_models

from ... import models
from ..mobile import MobileSerializer
from ..email import EmailSerializer
from ..phone import PhoneSerializer


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    mobiles = MobileSerializer(many=True)
    phones = PhoneSerializer(many=True)
    emails = EmailSerializer(many=True)

    # geo
    nationality = serializers.PrimaryKeyRelatedField(
        queryset=geo_models.Nationality.objects.all(),
    )
    city = serializers.PrimaryKeyRelatedField(
        queryset=geo_models.City.objects.all(),
    )
    # org
    cost_center = serializers.PrimaryKeyRelatedField(
        queryset=org_models.CostCenter.objects.all(),
    )
    position = serializers.PrimaryKeyRelatedField(
        queryset=org_models.Position.objects.all(),
    )
    status = serializers.PrimaryKeyRelatedField(
        queryset=org_models.Status.objects.all(),
    )
    job_subtype = serializers.PrimaryKeyRelatedField(
        queryset=org_models.JobSubtype.objects.all(),
    )
    # edu
    degree = serializers.PrimaryKeyRelatedField(
        queryset=edu_models.Degree.objects.all(),
    )
    school = serializers.PrimaryKeyRelatedField(
        queryset=edu_models.School.objects.all(),
    )
    specialization = serializers.PrimaryKeyRelatedField(
        queryset=edu_models.Specialization.objects.all(),
    )
    # core
    user = serializers.PrimaryKeyRelatedField(
        queryset=core_models.User.objects.all(),
        required=False,
    )

    def create(self, validated_data: dict):
        phones_data = validated_data.pop("phones")
        emails_data = validated_data.pop("emails")
        mobiles_data = validated_data.pop("mobiles")
        groups_data = validated_data.pop("groups")

        employee = models.Employee.objects.create(**validated_data)

        for phone_data in phones_data:
            data = {
                "employee": employee,
                "number": phone_data.get("number"),
                "notes": phone_data.get("notes", ""),
            }
            if phone_data.get("kind"):
                data["kind"] = phone_data.get("kind")
            models.Phone.objects.create(**data)

        for email_data in emails_data:
            data = {
                "employee": employee,
                "email": email_data.get("email"),
                "notes": email_data.get("notes", ""),
            }
            if email_data.get("kind"):
                data["kind"] = email_data.get("kind")
            models.Email.objects.create(**data)

        for mobile_data in mobiles_data:
            data = {
                "employee": employee,
                "number": mobile_data.get("number"),
                "has_whatsapp": mobile_data.get("has_whatsapp", True),
                "notes": mobile_data.get("notes", ""),
            }
            if mobile_data.get("kind"):
                data["kind"] = mobile_data.get("kind")
            models.Mobile.objects.create(**data)

        for group in groups_data:
            employee.groups.add(group)

        return employee

    class Meta:
        model = models.Employee
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
            ##### geo #####
            "nationality",
            "city",
            ##### geo #####
            "hire_date",
            "notes",
            "profile",
            "identity_document",
            ##### org #####
            "cost_center",
            "position",
            "status",
            "job_subtype",
            "groups",
            ##### org #####
            ##### edu #####
            "degree",
            "school",
            "specialization",
            ##### edu #####
            "user",
            "mobiles",
            "phones",
            "emails",
        )
