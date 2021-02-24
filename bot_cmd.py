import os
import random
import logging
import asyncio

# Setup logger
logger = logging.getLogger('bot_logger')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug_messages.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(fh)
logger.addHandler(ch)


from discord.message import Message
from discord.ext import commands
import finance_helper as ft
from bot_twitter import read_tweets
import greetings_cog


TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='$')
bot.add_cog(greetings_cog.Greetings(bot))


@bot.event
async def on_message(message: Message):
    if message.content.startswith('$thumb'):
        channel = message.channel
        await channel.send('Send me a thumbs up mate')

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('👎')
        else:
            await channel.send('👍')


@bot.event
async def on_error(event: str):
    logger.debug(f'Just another error {event}')


@bot.event
async def on_ready():
    logger.debug('Im ready')
    logger.debug('Logged in as')
    logger.debug(bot.user.name)
    logger.debug(bot.user.id)
    logger.debug('------')
    logger.debug(bot.guilds)
    logger.debug(bot.emojis)


@bot.event
async def on_disconnect():
    logger.debug('Disconnected...')


@bot.command()
async def test(ctx, a, b):
    old_style = ' OLD STYLE Got {} and {}'.format(a, b)
    logger.debug(f'Got {a} and {b}')
    logger.debug(old_style)

    await ctx.send('ready ' + str(a+b))


@test.error
async def info_error(ctx, error: str):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'That command is missing a parameter. {error}')

############################

@bot.command()
async def twitter(ctx):
    raise RuntimeError('I cannot read Twitter yet')

@twitter.error
async def twitter_error(ctx, error: str):
    await ctx.send(error)

########################################


@bot.command()
async def sendfile(ctx, ticker):
    from discord.file import File

    path = ft.finance_plot(ticker)
    with open(path, 'rb') as img:
        await ctx.send(file=File(img))


@bot.command()
async def stocks(ctx, ticker, param=None, start=None, end=None):
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

    await ctx.send(data)


################################

@stocks.error
async def ticker_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('That command is missing a parameter')

################################


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send(f'Received general error when adding: <{error}>')

#################################


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


#################################

@bot.command()
async def tweets(ctx, term: str = 'fifa'):
    tweets = read_tweets(term)
    for t in tweets:
        await ctx.send(t)


@tweets.error
async def tweets_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send(f'Received general error when querying tweets: <{error}>')


#################################

@bot.command()
async def commands(ctx):
    await ctx.send([command.name for command in bot.commands])


@commands.error
async def commands_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send(f'Received general error when querying commands: <{error}>')


bot.run(TOKEN)