from rest_framework import serializers

from apps.geo.models import Nationality
from apps.geo.serializers import NationalitySerializer

from .. import models


class SchoolSerializer(serializers.ModelSerializer):
    nationality = NationalitySerializer(read_only=True)
    is_governmental = serializers.BooleanField(required=False)
    is_virtual = serializers.BooleanField(required=False)

    class Meta:
        model = models.School
        fields = (
            "id",
            "name",
            "is_governmental",
            "is_virtual",
            "nationality",
            "website",
            "email",
            "phone",
            "description",
        )


class CreateUpdateSchoolSerializer(serializers.ModelSerializer):
    nationality = serializers.PrimaryKeyRelatedField(
        queryset=Nationality.objects.all(),
    )

    class Meta:
        model = models.School


class SchoolActivitySerializer(serializers.ModelSerializer):
    nationality = serializers.CharField(source="nationality.name")

    class Meta:
        model = models.School
        fields = (
            "id",
            "name",
            "is_governmental",
            "is_virtual",
            "nationality",
            "website",
            "email",
            "phone",
            "description",
        )
