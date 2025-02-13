from rest_framework import serializers

from . import models


class GovernorateSerializer(serializers.ModelSerializer):
    class BaseCitySerializer(serializers.ModelSerializer):
        class Meta:
            model = models.City
            fields = ("id", "name", "description")

    cities = BaseCitySerializer(many=True, read_only=True)

    class Meta:
        model = models.Governorate
        fields = ("id", "name", "description", "cities")


class GovernorateActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Governorate
        fields = ("name", "description")


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


class NationalitySerializer(serializers.ModelSerializer):
    is_local = serializers.BooleanField(required=False)

    class Meta:
        model = models.Nationality
        fields = ("id", "name", "is_local", "description")


class NationalityActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nationality
        fields = ("name", "is_local", "description")
