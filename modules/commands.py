import random

from main import logger

"""
Ideas

schedule morning messages based on timezone
send some messages for each command and check status
ping @channel for news
"""

import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def _ping(self, ctx):
        """Ping the Bot"""
        calc = await ctx.send(embed=discord.Embed(description="Ping"))
        clientping = (calc.created_at - ctx.message.created_at).total_seconds() * 1000
        await calc.edit(embed=discord.Embed(
            description=f"Bot Latency ``{round(self.bot.latency * 1000)}``\nClient Latency ``{clientping}``\n",
            delete_after=10))

    @commands.command(name="test")
    async def _test(self, ctx, a, b):
        old_style = 'OLD STYLE Got {} and {}'.format(a, b)
        logger.debug(f'Got {a} and {b}')
        logger.debug(old_style)

        await ctx.send('ready ' + str(a + b))

    @_test.error
    async def info_error(self, ctx, error: str):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'That command is missing a parameter. {error}')

    ################################

    @commands.command(name="add", usage=f"$add 1 3")
    async def _add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(left + right)

    @_add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f'Received general error when adding: <{error}>')

    @commands.command(name="roll")
    async def _roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            return await ctx.send('Format has to be in XdY. X = number of rolls. Y = limit')

        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        await ctx.send(result)

    #################################

    @commands.command(name="commands")
    async def _commands(self, ctx):
        await ctx.send([command.name for command in self.bot.commands])

    @_commands.error
    async def commands_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f'Received general error when querying commands: <{error}>')


def setup(bot):
    bot.add_cog(Commands(bot))
