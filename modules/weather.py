import itertools

from pathlib import Path
from discord.ext import commands
from helpers.openweather_client import OpenWeatherClient, OpenWeatherError

from config import logger

key_path = Path('helpers/key.ini')


class WeatherApi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            self.client = OpenWeatherClient(keyfile=key_path)
        except OpenWeatherError as e:
            logger.error(e)

    def _format_forecast(self, fc_nt):
        """
        forecast_nt = namedtuple('Forecast', 'dt main temp feels_like min_temp max_temp icon')
        """
        fmt = '{date}{}{main}{}{temp}'.format('\t'.ljust(10), '\t'.ljust(10), date=fc_nt.dt,
                                              main=fc_nt.main,
                                              temp=round(fc_nt.temp)
                                              )
        return fmt

    @commands.command(name='fc')
    async def forecast(self, ctx, city):
        if self.client:
            forecast = self.client.forecast(city)
            fmt = 'Date{}Desc{}Temp.'.format('\t'.ljust(10), '\t'.ljust(10))
            await ctx.send(fmt)

            for fc in itertools.islice(forecast, 0, len(forecast), 3):
                fc_repr = self._format_forecast(fc)
                await ctx.send(fc_repr)
        else:
            logger.error(f'No Weather client initialized')


def setup(bot):
    bot.add_cog(WeatherApi(bot))