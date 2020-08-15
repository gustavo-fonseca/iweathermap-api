from django.test import TestCase

from core.openweathermap import OpenWeatherMap


class OpenWeatherMapTestCase(TestCase):
    def setUp(self):
        self.cl_instance = OpenWeatherMap("Aracaju")

    def test_city_name(self):
        self.cl_instance.city_name = "São Paulo"
        self.assertEqual(self.cl_instance.city_name, "São Paulo")

        with self.assertRaises(TypeError):
            self.cl_instance.city_name = 3

        with self.assertRaises(TypeError):
            self.cl_instance.city_name = []

        with self.assertRaises(TypeError):
            self.cl_instance.city_name = {}

    def test_state_name(self):
        self.cl_instance.state_name = "br"
        self.assertEqual(self.cl_instance.state_name, "br")

        with self.assertRaises(TypeError):
            self.cl_instance.state_name = 3

        with self.assertRaises(TypeError):
            self.cl_instance.state_name = []

        with self.assertRaises(TypeError):
            self.cl_instance.state_name = {}

    def test_base_url(self):
        self.cl_instance.base_url = "https://test.io/api"
        self.assertEqual(self.cl_instance.base_url, "https://test.io/api")

        with self.assertRaises(TypeError):
            self.cl_instance.base_url = 3

        with self.assertRaises(TypeError):
            self.cl_instance.base_url = []

        with self.assertRaises(TypeError):
            self.cl_instance.base_url = {}

    def test_units(self):
        self.cl_instance.units = "metric"
        self.assertEqual(self.cl_instance.units, "metric")

        self.cl_instance.units = "imperial"
        self.assertEqual(self.cl_instance.units, "imperial")

        with self.assertRaises(ValueError):
            self.cl_instance.units = "other"

    def test_api_key(self):
        self.cl_instance.api_key = "xsS3*7asd2;4$"
        self.assertEqual(self.cl_instance.api_key, "xsS3*7asd2;4$")

        with self.assertRaises(TypeError):
            self.cl_instance.api_key = 3

        with self.assertRaises(TypeError):
            self.cl_instance.api_key = []

        with self.assertRaises(TypeError):
            self.cl_instance.api_key = {}

    def test_five_days_forecast_three_horus_data(self):
        forecasts = self.cl_instance.get_five_days_forecast_three_hours_data()

        self.assertNotEqual(forecasts, {})

        # Check if its return at least five days forecast
        self.assertGreaterEqual(len(forecasts.keys()), 5)

        # Check if each day returns 3 hours data
        self.assertEqual(len(next(iter(forecasts))), 10)

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

