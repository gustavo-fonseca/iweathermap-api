from rest_framework import routers

from forecast.views import ForecastViewSet


forecast_router = routers.SimpleRouter(trailing_slash=False)
forecast_router.register(r'forecast', ForecastViewSet, basename='forecast')
