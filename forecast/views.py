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
        """Next five days forecast

        Get next five days forecast. It includes weather data every 3 hours.

        Required query params: city_id

        """
        city_id = request.query_params.get("city_id", "")

        if city_id != "":
            weather_map = OpenWeatherMap(city_id)

            return Response(weather_map.get_five_days_forecast(),
                status=status.HTTP_200_OK)

        return Response({"message": "Please provide a valid city_id"},
            status=status.HTTP_400_BAD_REQUEST)


class CityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """City List

    OpenWeatherAPI cities list

    required query params: search=city name
    """

    queryset = City.objects.none()
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # only return results if search length is greater than 3 chars
        if len(self.request.query_params.get("search", "")) >= 3:
            return City.objects.filter(name__istartswith=self.request.query_params.get("search"))
        return City.objects.none()
