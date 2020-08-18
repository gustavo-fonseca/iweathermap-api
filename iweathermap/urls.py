from django.urls import path, include
from rest_framework import permissions
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from forecast.urls import forecast_router

# drf routes
router = routers.DefaultRouter(trailing_slash=False)
router.registry.extend(forecast_router.registry)

# drf_yasg scheme view
schema_view = get_schema_view(
    openapi.Info(title="IWeatherMap", default_version="v0.1"),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    # api router urls
    path("", schema_view.with_ui("redoc", cache_timeout=0)),
    path("", include(router.urls)),
]
