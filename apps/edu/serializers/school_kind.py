from rest_framework import serializers

from .. import models


class SchoolKindSerializer(serializers.ModelSerializer):
    class SchoolSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.School
            fields = (
                "id",
                "name",
                "nationality",
                "website",
                "email",
                "phone",
                "description",
            )

    is_governmental = serializers.BooleanField()
    is_virtual = serializers.BooleanField()
    schools = SchoolSerializer(many=True, read_only=True)
    schools_count = serializers.IntegerField(read_only=True)
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.SchoolKind
        fields = (
            "id",
            "name",
            "is_governmental",
            "is_virtual",
            "description",
            "schools",
            "schools_count",
            "employees_count",
        )
