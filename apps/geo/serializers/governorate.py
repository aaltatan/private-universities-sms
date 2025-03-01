from rest_framework import serializers

from .. import models


class GovernorateSerializer(serializers.ModelSerializer):
    class BaseCitySerializer(serializers.ModelSerializer):
        class Meta:
            model = models.City
            fields = ("id", "name", "description")

    cities_count = serializers.IntegerField(read_only=True)
    cities = BaseCitySerializer(many=True, read_only=True)

    class Meta:
        model = models.Governorate
        fields = ("id", "name", "description", "cities", "cities_count")


class GovernorateActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Governorate
        fields = ("name", "description")
