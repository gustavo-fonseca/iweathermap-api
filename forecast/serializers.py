from rest_framework import serializers

from forecast.models import City


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ["code", "name", "state", "country"]
