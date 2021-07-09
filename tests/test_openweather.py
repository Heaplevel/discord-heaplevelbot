import unittest

from pathlib import Path

from helpers.openweather_client import OpenWeatherClient


class OpenWeatherApiTest(unittest.TestCase):

    def setUp(self) -> None:
        key_path = Path(__file__).parent / 'key.ini'
        self.client = OpenWeatherClient(keyfile=key_path)
        print('Starting test')

    def test_connection(self):
        forecast = self.client.forecast('Stockholm', 'SE')

        """
        Format for string 
        date, main temp, feels like, min temp, max temp
        """
        for fc_nt in forecast:
            fmt = '{date}{}{main}{}{temp}'.format('\t'.ljust(10), '\t'.ljust(10), date=fc_nt.dt,
                                                  main=fc_nt.main,
                                                  temp=round(fc_nt.temp)
                                                  )
            print(fmt)
            self.assertIsNotNone(fc_nt.main)

if __name__ == '__main__':
    unittest.main()