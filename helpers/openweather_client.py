import configparser
import requests
from datetime import datetime
from collections import namedtuple


class OpenWeatherError(Exception):

    def __init__(self, message):
        self.message = message


class OpenWeatherClient(object):

    def __init__(self, keyfile):
        config = configparser.ConfigParser()
        if len(config.read(keyfile)) == 0:
            raise OpenWeatherError(f'Error when reading key file for API Client')

        ow = config['Openweather']
        self.key = ow['key']

    def forecast(self, city='Stockholm', country='SE'):
        api_url = f'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={self.key}&q={city},{country}&units=metric'
        response = requests.get(api_url)
        result = response.json()
        days = result['list']

        forecast = []
        forecast_nt = namedtuple('Forecast', 'dt main temp feels_like min_temp max_temp icon')

        for day in days:
            dt = datetime.utcfromtimestamp(day["dt"])
            weather_main, weather_icon = day["weather"][0]["main"], day["weather"][0]["icon"]
            icon_url = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
            icon_b = requests.get(icon_url)

            forecast.append(
                forecast_nt(dt, weather_main, day["main"]["temp"], day["main"]["feels_like"], day["main"]["temp_min"],
                            day["main"]["temp_max"],
                            weather_icon)
            )
        return forecast
