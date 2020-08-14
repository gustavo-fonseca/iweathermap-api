from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from core.openweathermap import OpenWeatherMap


class NextFiveDaysForecastViewSet(viewsets.GenericViewSet):

    @swagger_auto_schema(responses={200: '', 400: ''})
    @action(
        methods=["get"],
        detail=False,
        url_path="next-five-days",
        url_name="next-five-days",
        permission_classes=[permissions.AllowAny]
    )
    def next_five_days_forecast(self, request):
        """
        Get next five days forecast with max humidity data
        """
        city_name = request.query_params.get("city_name")
        state_name = request.query_params.get("state_name")

        if city_name:
            open_weather_map = OpenWeatherMap(city_name, state_name=state_name)

            return Response(
                open_weather_map.get_next_five_days_max_humidity(),
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "message": "Please provide a valid city name"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
