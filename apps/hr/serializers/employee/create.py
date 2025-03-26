from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.core import validators

from ... import models


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    class MobileSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        number = serializers.CharField(
            validators=[validators.syrian_mobile_validator],
        )
        kind = serializers.ChoiceField(
            choices=models.Mobile.KindChoices.choices,
            required=False,
        )
        has_whatsapp = serializers.BooleanField(
            initial=True,
            required=False,
        )
        notes = serializers.CharField(required=False, allow_blank=True)

    class PhoneSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        number = serializers.CharField(
            validators=[validators.syrian_phone_validator],
        )
        kind = serializers.ChoiceField(
            choices=models.Mobile.KindChoices.choices,
            required=False,
        )
        notes = serializers.CharField(required=False, allow_blank=True)

    class EmailSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        email = serializers.EmailField()
        kind = serializers.ChoiceField(
            choices=models.Email.KindChoices.choices,
            required=False,
        )
        notes = serializers.CharField(required=False, allow_blank=True)

    mobiles = MobileSerializer(many=True)
    phones = PhoneSerializer(many=True)
    emails = EmailSerializer(many=True)

    def validate_emails(self, emails: list[dict]):
        if emails:
            stmt = Q()
            for email in emails:
                stmt |= Q(email=email.get("email"))

            exists = (
                models.Email.objects.filter(stmt)
                .exclude(employee=self.instance)
                .exists()
            )
            if exists:
                raise serializers.ValidationError(
                    _("some emails already exist"),
                )
        return emails

    def validate_phones(self, phones: list[dict]):
        if phones:
            stmt = Q()
            for phone in phones:
                stmt |= Q(number=phone.get("number"))

            stmt &= Q(employee=self.instance)

            exists = (
                models.Phone.objects.filter(stmt)
                .exclude(employee=self.instance)
                .exists()
            )
            if exists:
                raise serializers.ValidationError(
                    _("some phones already exist"),
                )
        return phones

    def validate_mobiles(self, mobiles: list[dict]):
        if mobiles:
            stmt = Q()
            for mobile in mobiles:
                stmt |= Q(number=mobile.get("number"))

            exists = (
                models.Mobile.objects.filter(stmt)
                .exclude(employee=self.instance)
                .exists()
            )
            if exists:
                raise serializers.ValidationError(
                    _("some mobiles already exist"),
                )
        return mobiles

    def update(self, instance: models.Employee, validated_data: dict):
        phones_data = validated_data.pop("phones", None)
        emails_data = validated_data.pop("emails", None)
        mobiles_data = validated_data.pop("mobiles", None)
        groups_data = validated_data.pop("groups", None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if phones_data is not None:
                instance.phones.all().delete()
                for phone in phones_data:
                    data = {
                        "employee": instance,
                        "number": phone.get("number"),
                        "notes": phone.get("notes", ""),
                    }
                    if phone.get("kind"):
                        data["kind"] = phone.get("kind")
                    models.Phone.objects.create(**data)

            if emails_data is not None:
                instance.emails.all().delete()
                for email in emails_data:
                    data = {
                        "employee": instance,
                        "email": email.get("email"),
                        "notes": email.get("notes", ""),
                    }
                    if email.get("kind"):
                        data["kind"] = email.get("kind")
                    models.Email.objects.create(**data)

            if mobiles_data is not None:
                mobiles_data = validated_data.pop("mobiles", [])
                instance.mobiles.all().delete()
                for mobile in mobiles_data:
                    data = {
                        "employee": instance,
                        "number": mobile.get("number"),
                        "has_whatsapp": mobile.get("has_whatsapp", True),
                        "notes": mobile.get("notes", ""),
                    }
                    if mobile.get("kind"):
                        data["kind"] = mobile.get("kind")
                    models.Mobile.objects.create(**data)

            if groups_data is not None:
                instance.groups.clear()
                for group in groups_data:
                    instance.groups.add(group)

            return instance

    def create(self, validated_data: dict):
        phones_data = validated_data.pop("phones", [])
        emails_data = validated_data.pop("emails", [])
        mobiles_data = validated_data.pop("mobiles", [])
        groups_data = validated_data.pop("groups", [])

        with transaction.atomic():
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
