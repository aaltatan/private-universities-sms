from rest_framework import serializers

from .models import City, Governorate


class CitySerializer(serializers.ModelSerializer):
    class GovernorateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Governorate
            fields = ("id", "name", "description")

    governorate = GovernorateSerializer(read_only=True)

    class Meta:
        model = City
        fields = ("id", "name", "description", "governorate")


class ActivitySerializer(serializers.ModelSerializer):
    governorate = serializers.SerializerMethodField()

    def get_governorate(self, obj: City):
        return obj.governorate.name

    class Meta:
        model = City
        fields = ("name", "governorate", "description")
