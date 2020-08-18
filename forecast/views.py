from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from core.openweathermap import OpenWeatherMap
from forecast.models import City
from forecast.serializers import CitySerializer


class ForecastViewSet(viewsets.ViewSet):

    @swagger_auto_schema(responses={200: '', 400: 'Please provide a valid city name"'})
    @action(
        methods=["get"],
        detail=False,
        url_path="next-five-days",
        url_name="next-five-days",
        permission_classes=[permissions.AllowAny]
    )
    def next_five_days_forecast(self, request):
        """
        Get next five days forecast. It includes weather data every 3 hours.
        """
        city_name = request.query_params.get("city_name", "")
        state_name = request.query_params.get("state_name", "")

        if city_name:
            weather_map = OpenWeatherMap(city_name, state_name=state_name)

            return Response(weather_map.get_five_days_forecast(),
                status=status.HTTP_200_OK)

        return Response({"message": "Please provide a valid city name"},
            status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(responses={200: '', 400: 'Please provide a valid city name"'})
    @action(
        methods=["get"],
        detail=False,
        url_path="next-days-rain-chances",
        url_name="next-days-rain-chances",
        permission_classes=[permissions.AllowAny]
    )
    def next_days_rain_chances(self, request):
        """
        Get next five days forecast with max humidity data over 70%
        """
        city_name = request.query_params.get("city_name", "")
        state_name = request.query_params.get("state_name", "")

        if city_name:
            open_weather_map = OpenWeatherMap(city_name, state_name=state_name)

            return Response(open_weather_map.get_days_rain_chances(),
                status=status.HTTP_200_OK)

        return Response({"message": "Please provide a valid city name"},
            status=status.HTTP_400_BAD_REQUEST)


class CityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = City.objects.none()
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # only return results if search length is greater than 3 chars
        if len(self.request.query_params.get("search", "")) >= 3:
            return City.objects.filter(name__istartswith=self.request.query_params.get("search"))
        return City.objects.none()
