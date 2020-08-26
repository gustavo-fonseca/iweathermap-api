from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class ForecastTests(APITestCase):

    def setUp(self):
        self.params_payload = {"city_id": "3451328"}

    def test_next_five_days(self):
        response = self.client.get(
            reverse("forecast-next-five-days"), self.params_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse("forecast-next-five-days"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CityTests(APITestCase):

    def setUp(self):
        self.params_payload = {"search": "Ribeirão Preto"}

    def test_city_list(self):
        response = self.client.get(reverse("city-list"), self.params_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse("city-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("results"), [])
