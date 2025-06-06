from rest_framework import serializers

from apps.geo.models import Nationality
from apps.geo.serializers import NationalitySerializer

from .. import models


class SchoolSerializer(serializers.ModelSerializer):
    class KindSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.SchoolKind
            fields = ("id", "name", "is_governmental", "is_virtual", "description")

    nationality = NationalitySerializer(read_only=True)
    kind = KindSerializer(read_only=True)
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.School
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
            "employees_count",
        )


class CreateUpdateSchoolSerializer(serializers.ModelSerializer):
    kind = serializers.PrimaryKeyRelatedField(
        queryset=models.SchoolKind.objects.all(),
    )
    nationality = serializers.PrimaryKeyRelatedField(
        queryset=Nationality.objects.all(),
    )

    class Meta:
        model = models.School
        fields = (
            "name",
            "kind",
            "nationality",
            "website",
            "email",
            "phone",
            "address",
            "description",
        )
