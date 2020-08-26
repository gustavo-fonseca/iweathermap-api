from django.test import TestCase

from core.openweathermap import OpenWeatherMap


class OpenWeatherMapTestCase(TestCase):

    def setUp(self):
        self.cl_instance = OpenWeatherMap("3451328")

    def test_five_days_forecast(self):
        forecasts = self.cl_instance.get_five_days_forecast()

        self.assertNotEqual(forecasts.get("data"), {})

        # Check if its return at least five days forecast
        self.assertGreaterEqual(len(forecasts.get("data").keys()), 5)

        # Check if each day returns 3 hours data
        self.assertEqual(len(next(iter(forecasts.get("data")))), 10)

    def test_five_days_forecast_max_humidity(self):
        forecasts = self.cl_instance.get_five_days_forecast_max_humidity()

        self.assertEqual(isinstance(forecasts, list), True)

        # Check if its return at least five days forecast
        self.assertGreaterEqual(len(forecasts), 5)

    def test_days_rain_chances(self):
        forecasts = self.cl_instance.get_days_rain_chances()

        self.assertNotEqual(forecasts, {})

        # Check if returns all items
        if len(forecasts) > 0:
            self.assertIn("temp", forecasts[0])
            self.assertIn("feels_like", forecasts[0])
            self.assertIn("temp_min", forecasts[0])
            self.assertIn("temp_max", forecasts[0])
            self.assertIn("humidity", forecasts[0])
            self.assertIn("datetime", forecasts[0])
