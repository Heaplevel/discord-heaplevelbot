import configparser
import requests
from datetime import datetime


class OpenWeatherError(Exception):

    def __init__(self, message):
        self.message = message


class OpenWeatherClient(object):

    def __init__(self):
        config = configparser.ConfigParser()
        if len(config.read('key.ini')) == 0:
            raise OpenWeatherError(f'Error when reading key file for API Client')

        ow = config['Openweather']
        self.key = ow['key']

    def forecast(self, city='Stockholm', country='SE'):
        api_url = f'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={self.key}&q={city},{country}&units=metric'
        response = requests.get(api_url)
        result = response.json()
        days = result['list']

        forecast = []
        for day in days:
            dt = datetime.utcfromtimestamp(day["dt"])
            print(dt)
            weather_main, weather_icon = day["weather"][0]["main"], day["weather"][0]["icon"]
            icon_url = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
            icon_b = requests.get(icon_url)

            forecast.append(f'{day["main"]["temp"]} {day["main"]["feels_like"]} {day["main"]["temp_min"]} {day["main"]["temp_max"]}')
