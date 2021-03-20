from discord.ext import commands
from helpers.helpers import split_2000, read_tweets


class Tweets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="twitter")
    async def _twitter(self, ctx):
        raise RuntimeError('I cannot read Twitter yet')

    @_twitter.error
    async def twitter_error(self, ctx, error: str):
        await ctx.send(error)

    @commands.command(name="tweets")
    async def _tweets(self, ctx, term: str = 'fifa'):
        tweets = read_tweets(term)
        for t in tweets:
            await ctx.send(t)

    @_tweets.error
    async def tweets_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f'Received general error when querying tweets: <{error}>')


def setup(bot):
    bot.add_cog(Tweets(bot))
