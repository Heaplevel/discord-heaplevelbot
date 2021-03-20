import datetime

from discord.ext import commands

from helpers import finance_helper as ft
from helpers.helpers import split_2000
from main import logger


class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stocks")
    async def _stocks(self, ctx, ticker, param=None, start=None, end=None):
        logger.debug(f'{ctx.message.content} <{ticker}>')

        if param and param == 'history':
            data = ft.finance_history(ticker, start, end)
        elif param == 'calendar':
            data = ft.finance_calendar(ticker)
        else:
            await ctx.send(f'Retrieving stock info {ticker}')
            data = ft.finance_helper(ticker)
            await ctx.send(f'Tada!')
            logger.debug(data)

        data = split_2000(data)
        for d in data:
            await ctx.send(d)

    @commands.command(name="send")
    async def _sendfile(self, ctx, ticker):
        from discord.file import File

        path = ft.finance_plot(ticker, start=datetime.date.today() - datetime.timedelta(days=30),
                               end=datetime.date.today())
        with open(path, 'rb') as img:
            await ctx.send(file=File(img))

    @_stocks.error
    async def ticker_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('That command is missing a parameter')


def setup(bot):
    bot.add_cog(Stocks(bot))
