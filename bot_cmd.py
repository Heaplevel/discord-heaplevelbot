import os
import random

import yfinance

from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='$')
cache = {}

def finance_history(stock):
    ticker = get_ticker(stock)
    return ticker.history()


def get_ticker(stock):
    ticker = cache.get(stock, None)
    if not ticker:
        ticker = yfinance.Ticker(stock)
        cache.setdefault(stock, ticker)
    return cache.get(stock)



def finance_helper(stock):
    l = []

    ticker = cache.get(stock, None)
    if not ticker:
        ticker = yfinance.Ticker(stock)
        cache.setdefault(stock, ticker)

    for k, v in ticker.info.items():
        l.append(':'.join([k, str(v)]))

    recommendations = ticker.recommendations.tail(5).to_string()

    ticker_info = '\n'.join(l[:3])
    summary = '\n'.join([ticker_info, '', '### RECOMMENDATIONS ### ', recommendations])
    return summary


@bot.event
async def on_error(event: str):
    print('Just another error ' + event)


@bot.event
async def on_ready():
    print('Im ready')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print(bot.guilds)
    print(bot.emojis)


@bot.command()
async def test(ctx, a, b):
    old_style = ' OLD STYLE Got {} and {}'.format(a, b)
    print(f'Got {a} and {b}')
    print(old_style)

    await ctx.send('ready ' + str(a+b))


@test.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('That command is missing a parameter')


@bot.command()
async def stocks(ctx, ticker, history=None):
    print(ctx.message.content, ticker)
    if history and history == 'history':
        data = finance_history(ticker)
    else:
        data = finance_helper(ticker)

    await ctx.send(data)


@stocks.error
async def ticker_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('That command is missing a parameter')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in XdY. X = number of rolls. Y = limit')
        return

    result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
    await ctx.send(result)

bot.run(TOKEN)