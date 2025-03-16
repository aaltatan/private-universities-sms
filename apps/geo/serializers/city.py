from rest_framework import serializers

from .. import models


class CitySerializer(serializers.ModelSerializer):
    class BaseGovernorateSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Governorate
            fields = ("id", "name", "description")

    governorate = BaseGovernorateSerializer(read_only=True)
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.City
        fields = (
            "id",
            "name",
            "kind",
            "description",
            "governorate",
            "employees_count",
        )


class CreateUpdateCitySerializer(serializers.ModelSerializer):
    governorate = serializers.PrimaryKeyRelatedField(
        queryset=models.Governorate.objects.all(),
    )

    class Meta:
        model = models.City
        fields = ("name", "kind", "governorate", "description")
