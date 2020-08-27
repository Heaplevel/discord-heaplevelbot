# bot.py
import os
import yfinance

import discord

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
cache = {}


def finance_helper(stock):
    l = []

    ticker = cache.get(stock, None)
    if not ticker:
        ticker = yfinance.Ticker(stock)
        cache.setdefault(stock, ticker)

    for k,v in ticker.info.items():
        l.append(':'.join([k,str(v)]))

    recommendations = ticker.recommendations.tail(5).to_string()

    ticker_info = '\n'.join(l[:3])
    summary = '\n'.join([ticker_info, '', '### RECOMMENDATIONS ### ', recommendations])
    return summary


@client.event
async def on_ready():
    for guild in client.guilds:
        print(guild)
        if guild.name == "Heaplevel":
            print('Yes you are in the Heaplevel server or guild whichever term you wish to use')

    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    print(message)
    channel = message.channel
    if message.content.startswith('!ping'):
        await channel.send('Pong.')

    if message.content.startswith('!stocks'):
        splitted = message.content.split(' ')
        if len(splitted) == 1:
            await channel.send('Please provide a stock name, MSFT AAPL GOOGL etc')
        elif len(splitted) == 2:
            info = finance_helper(splitted[1])
            await channel.send(info)
        else:
            await channel.send(
                'Some day I\'ll show you the most popular stocks from Yahoo Finance. Please insert new coin')

    if message.content.startswith('!beep'):
        await channel.send('Boop.')

    if message.content.startswith('$greet'):
        await channel.send('Say hello!')

        def check(m):
            return m.content.lower() == 'hello' and m.channel == channel

        msg = await client.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))



client.run(TOKEN)


# https://discord.com/oauth2/authorize?client_id=742715929481314314&scope=bot