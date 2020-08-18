import requests

from django.conf import settings

from core.utils.date import strptime_utc_to_tz
from core.utils.string import words_separator
from core.contants import WEATHER_ICONS


class OpenWeatherMapBase:
    """OpenWeatherMap Base class
    Implements OpenWeatherMap's base attrs getters and setters and its validation
    """

    def __init__(self,
                 city_id,
                 base_url="http://api.openweathermap.org/data/2.5/",
                 units="metric",
                 rain_humidity=70,
                 api_key=None,
                 timezone=None):
        self.city_id = city_id
        self.base_url = base_url
        self.units = units
        self.rain_humidity = rain_humidity
        self.api_key = api_key or settings.OPENWEATHERMAP_API_KEY
        self.timezone = timezone or settings.TIME_ZONE
        self.forecasts = None

    @property
    def city_id(self) -> str:
        return self.__city_id

    @city_id.setter
    def city_id(self, city_id: str):
        if isinstance(city_id, str):
            self.__city_id = city_id
        else:
            raise TypeError("city_id must a str instance")

    @property
    def base_url(self) -> str:
        return self.__base_url

    @base_url.setter
    def base_url(self, base_url: str):
        if isinstance(base_url, str):
            self.__base_url = base_url
        else:
            raise TypeError("base_url must a str instance")

    @property
    def units(self) -> str:
        return self.__units

    @units.setter
    def units(self, units: str):
        if units in ("metric", "imperial"):
            self.__units = units
        else:
            raise ValueError("units must be set as 'metric' or 'imperial'")

    @property
    def rain_humidity(self) -> str:
        return self.__rain_humidity

    @rain_humidity.setter
    def rain_humidity(self, rain_humidity: int):
        if isinstance(rain_humidity, int):
            self.__rain_humidity = rain_humidity
        else:
            raise TypeError("rain_humidity must a int instance")

    @property
    def api_key(self) -> str:
        return self.__api_key

    @api_key.setter
    def api_key(self, api_key: str):
        if isinstance(api_key, str):
            self.__api_key = api_key
        else:
            raise TypeError("api_key must a str instance")


class OpenWeatherMap(OpenWeatherMapBase):
    """OpenWeatherMap API Integration"""

    def __get_endpoint(self, service_name: str) -> str:
        """Generate openweathermap's api endpoint based on service name

        Args:
            service_name (str): openweathermap service name - options: forecast

        Returns:
            str: openweathermap's api endpoint

        """
        return f"{self.base_url}{service_name}"


    def __get_default_payload(self) -> dict:
        """Get default params payload for openweathermap's api

        Returns:
            dict: default params' payload

        """
        return {"appid": self.api_key, "units": self.units}


    def __compute_raining_days(self) -> list:
        """Compute raining days based on humidity forecast

        Returns:
            str:

            "Monday, Tuesday and Friday"

        """

        raining_days = []

        for _, forecast in self.forecasts.items():
            # get the max humidity forecast per day
            forecast_max_humidity = max(forecast, key=lambda d: d['humidity'])
            if forecast_max_humidity.get('humidity') > self.rain_humidity:
                raining_days.append(forecast_max_humidity.get('weekday'))

        return words_separator(raining_days)


    def get_five_days_forecast(self) -> dict:
        """5 day forecast is available at any location or city.
        It includes weather data every 3 hours.

        Returns:
            dict: 5 days forecast filtered by date / 3 hours data

            # if the given city_id and state_name is valid
            {
                "2020-8-20": [
                    {
                        "temp": 19.16, "feels_like": 18.2, "temp_min": 18,
                        "temp_max": 19.16, "humidity": 55, "weekday": "Monday",
                        "datetime": datetime.datetime(2020, 8, 20, 9, 0),
                        "weather_icon": "clouds"
                    },
                    {...}
                ],
                "2020-8-21": [...]
            }

            # if the given city_id or state_name is not valid
            {

            }

        """

        params_payload = self.__get_default_payload()
        params_payload["id"] = self.city_id

        response = requests.get(self.__get_endpoint("forecast"),
            params=params_payload)

        payload = {
            "data": {},
            "raining_days_text": "",
            "city_name": ""
        }

        if response.status_code == requests.codes.ok:
            # Checks if respose's status_code is 200 (OK)

            data = response.json()

            for forecast in data.get('list'):
                forecast_main = forecast.get('main')

                # setting up datetime timezone
                forecast_dt = strptime_utc_to_tz(
                    date_string=forecast.get('dt_txt'),
                    format_string="%Y-%m-%d %H:%M:%S",
                    tz_string=self.timezone
                )

                forecast_dt_txt = forecast_dt.strftime("%Y-%m-%d")

                payload["data"].setdefault(forecast_dt_txt, [])

                payload["data"][forecast_dt_txt].append({
                    "temp": forecast_main.get('temp'),
                    "feels_like": forecast_main.get('feels_like'),
                    "temp_min": forecast_main.get('temp_min'),
                    "temp_max": forecast_main.get('temp_max'),
                    "humidity": int(forecast_main.get('humidity')),
                    "datetime": forecast_dt,
                    "weekday": forecast_dt.strftime("%A"),
                    "weather_icon": WEATHER_ICONS[forecast.get('weather')[0].get("main")]
                })

            self.forecasts = payload["data"]

            payload["raining_days_text"] = self.__compute_raining_days()
            payload["city_name"] = data.get("city").get("name")

        return payload


    def get_five_days_forecast_max_humidity(self) -> list:
        """Get next five days forecast
        give back the max humidity forecast by day

        Returns:
            list: 5 days forecast with max humidity data

            [
                {
                 'temp': 19.16, 'feels_like': 18.2, 'temp_min': 18,
                 'temp_max': 19.16, 'humidity': 55, 'weekday': 'Monday'
                 'datetime': datetime.datetime(2020, 8, 13, 9, 0)
                }
            ]

        """

        forecasts = []
        forecast_five_days = self.get_five_days_forecast().get("data")

        for dt_txt, forecast in forecast_five_days.items():
            # get the max humidity forecast per day
            forecast_max_humidity = max(forecast, key=lambda d: d['humidity'])
            forecasts.append(forecast_max_humidity)

        return forecasts


    def get_days_rain_chances(self):
        """Get list of next few days with rain chances

        Returns:
            list:

            [
                {
                    'temp': 19.16, 'feels_like': 18.2, 'temp_min': 18,
                    'temp_max': 19.16, 'humidity': 55, 'weekday': 'Monday'
                    'datetime': datetime.datetime(2020, 8, 13, 9, 0),
                    'weather_icon': 'clouds'
                }
            ]

        """

        forecasts = self.get_five_days_forecast_max_humidity()

        rain_chances = []

        for forecast in forecasts:
            if forecast.get('humidity') > self.rain_humidity:
                rain_chances.append(forecast)

        return rain_chances


    def display_raining_days(self):
        """
        Challenge Proposal
        """

        # request forecast from api
        self.get_five_days_forecast()

        raining_days_text = self.__compute_raining_days()

        print(f"You should take an umbrella in these days: {raining_days_text}")
