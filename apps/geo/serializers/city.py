from rest_framework import serializers

from .. import models


class CitySerializer(serializers.ModelSerializer):
    class BaseGovernorateSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Governorate
            fields = ("id", "name", "description")

    governorate = BaseGovernorateSerializer(read_only=True)

    class Meta:
        model = models.City
        fields = ("id", "name", "description", "governorate")


class CreateUpdateCitySerializer(serializers.ModelSerializer):
    governorate = serializers.PrimaryKeyRelatedField(
        queryset=models.Governorate.objects.all(),
    )

    class Meta:
        model = models.City
        fields = ("name", "governorate", "description")


class CityActivitySerializer(serializers.ModelSerializer):
    governorate = serializers.CharField(source="governorate.name")

    class Meta:
        model = models.City
        fields = ("name", "governorate", "description")
