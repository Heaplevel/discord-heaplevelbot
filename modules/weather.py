from discord.ext import commands
from helpers.openweather_client import OpenWeatherClient, OpenWeatherError

from config import logger


class WeatherApi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            self.client = OpenWeatherClient()
        except OpenWeatherError as e:
            logger.error('Cannot read the client key ')
            logger.error(e)

    @commands.command(name='fc')
    async def forecast(self, ctx, city):
        if self.client:
            forecast = self.client.forecast()
            await ctx.send(forecast)
        else:
            logger.error(f'No Weather client initialized')

def setup(bot):
    bot.add_cog(WeatherApi(bot))