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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["cities"] = {
            "count": representation.pop("cities_count"),
            "results": representation.pop("cities"),
        }
        return representation


class GovernorateActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Governorate
        fields = ("name", "description")
