import unittest
import requests
import configparser

class OpenWeatherApiTest(unittest.TestCase):


    def setUp(self) -> None:
        config = configparser.ConfigParser()
        config.read('key.ini')
        ow = config['Openweather']
        self.key = ow['key']

        print('Starting test')


    def test_connection(self):
        url = f'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={self.key}&q=Stockholm,SE&units=metric'

        response = requests.get(url)
        print(response.headers)
        result = response.json()

        days = result['list']
        print(days)
        from datetime import datetime
        for day in days:
            dt = datetime.utcfromtimestamp(day["dt"])
            print(dt)
            weather_main, weather_icon = day["weather"][0]["main"], day["weather"][0]["icon"]
            icon_url = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
            icon_b = requests.get(icon_url)
            print(icon_b.content)

            print(f'{day["main"]["temp"]} {day["main"]["feels_like"]} {day["main"]["temp_min"]} {day["main"]["temp_max"]}')
