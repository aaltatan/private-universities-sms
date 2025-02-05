from rest_framework import serializers

from apps.cities.models import City

from .models import Governorate


class GovernorateSerializer(serializers.ModelSerializer):
    class CitySerializer(serializers.ModelSerializer):
        class Meta:
            model = City
            fields = ("id", "name", "description")

    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Governorate
        fields = ("id", "name", "description", "cities")


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Governorate
        fields = ("name", "description")
