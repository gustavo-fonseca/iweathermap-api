from datetime import datetime
from django.conf import settings

import requests


class OpenWeatherMap:

    def __init__(self,
                 city_name,
                 state_name="br",
                 api_base_url="http://api.openweathermap.org/data/2.5/",
                 api_key=None,
                 api_units="metric"):
        self.city_name = city_name
        self.state_name = state_name
        self.api_base_url = api_base_url
        self.api_key = api_key | settings.OPENWEATHERMAP_API_KEY
        self.api_units = api_units

    @property
    def api_units(self) -> str:
        return self.__api_units

    @api_units.setter
    def api_units(self, api_units: str):
        if api_units in ("metric", "imperial"):
            self.__api_units = api_units
        else:
            raise ValueError("api_units must be set as 'metric' or 'imperial'")

    def __get_endpoint(self, service_name: str) -> str:
        """Generate openweathermap's api endpoint based on service name

        Args:
            service_name (str): openweathermap service name - options: forecast

        Returns:
            str: openweathermap's api endpoint

        """
        return f"{self.api_base_url}{service_name}"

    def __get_params_payload(self) -> dict:
        """Returns url default params for openweathermap's api

        Args:
            pass

        Returns:
            dict: default params' payload

        """
        return {
            "appid": self.api_key,
            "units": self.api_units
        }

    def get_next_five_days_forecast(self) -> dict:
        """5 day forecast is available at any location or city.
        It includes weather data every 3 hours.

        Args:
            pass

        Returns:
            dict: 5 days forecast filtered by date / 3 hours data

            # if the given city_name and state_name is valid
            {
                "2020-8-20": [
                    {
                        "temp": 19.16, "feels_like": 18.2, "temp_min": 18,
                        "temp_max": 19.16, "humidity": 55,
                        "datetime": datetime.datetime(2020, 8, 20, 9, 0)
                    },
                    {...}
                ],
                "2020-10-11": [...]
            }

            # if the given city_name or state_name is invalid
            {

            }

        """

        params_payload = self.__get_params_payload()
        params_payload["q"] = f"{self.city_name},{self.state_name}"

        response = requests.get(
            self.__get_endpoint("forecast"),
            params=params_payload
        )

        forecasts = {}

        if response.status_code == requests.codes.ok:
            # Checks if respose's status_code is 200 (OK)
            for forecast in response.json().get('list'):
                forecast_main = forecast.get('main')

                forecast_dt = datetime.strptime(
                    forecast.get("dt_txt"), "%Y-%m-%d %H:%M:%S")
                forecast_dt_txt = forecast_dt.strftime("%Y-%m-%d")

                forecasts.setdefault(forecast_dt_txt, [])

                forecasts[forecast_dt_txt].append({
                    "temp": forecast_main.get('temp'),
                    "feels_like": forecast_main.get('feels_like'),
                    "temp_min": forecast_main.get('temp_min'),
                    "temp_max": forecast_main.get('temp_max'),
                    "humidity": forecast_main.get('humidity'),
                    "datetime": forecast_dt
                })

        return forecasts

    def get_next_five_days_max_humidity(self) -> list:
        """
        Returns the next five days forecast and the current weather
        give back the max humidity forecast by day

        Args:
            pass

        Returns:
            list: 5 days forecast with max humidity data

            [
                {
                 'temp': 19.16, 'feels_like': 18.2, 'temp_min': 18,
                 'temp_max': 19.16, 'humidity': 55,
                 'datetime': datetime.datetime(2020, 8, 13, 9, 0)
                }
            ]
        """
        forecasts = []
        forecast_next_five_days = self.get_next_five_days_forecast()

        for dt_txt, forecast in forecast_next_five_days.items():
            # get the max humidity forecast per day
            forecast_max_humidity = max(forecast, key=lambda d: d['humidity'])
            forecasts.append(forecast_max_humidity)

        return forecasts
