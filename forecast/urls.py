from rest_framework import routers

from forecast.views import NextFiveDaysForecastViewSet


forecast_router = routers.SimpleRouter(trailing_slash=False)
forecast_router.register(r'forecast', NextFiveDaysForecastViewSet,
    basename='forecast')
