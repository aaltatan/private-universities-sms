from rest_framework import serializers

from .models import City, Governorate


class GovernorateSerializer(serializers.ModelSerializer):
    class BaseCitySerializer(serializers.ModelSerializer):
        class Meta:
            model = City
            fields = ("id", "name", "description")

    cities = BaseCitySerializer(many=True, read_only=True)

    class Meta:
        model = Governorate
        fields = ("id", "name", "description", "cities")


class CitySerializer(serializers.ModelSerializer):
    class BaseGovernorateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Governorate
            fields = ("id", "name", "description")

    governorate = BaseGovernorateSerializer(read_only=True)

    class Meta:
        model = City
        fields = ("id", "name", "description", "governorate")


class GovernorateActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Governorate
        fields = ("name", "description")


class CityActivitySerializer(serializers.ModelSerializer):
    governorate = serializers.CharField(source="governorate.name")

    class Meta:
        model = City
        fields = ("name", "governorate", "description")
