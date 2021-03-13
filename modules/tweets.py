from discord.ext import commands
from searchtweets import load_credentials, gen_rule_payload, collect_results

from helpers.helpers import split_2000

premium_search_args = load_credentials(filename="./search_tweets_creds_example.yaml",
                                       yaml_key="search_tweets_ent_example",
                                       env_overwrite=False)


def read_tweets(term):
    """
    @return: string output split into 2000 messages.
    """
    rule = gen_rule_payload(term, results_per_call=100)  # testing with a sandbox account
    print(rule)
    tweets = collect_results(rule, 100, premium_search_args)
    print(tweets[:10])
    output = '\n\n'.join([f'@{t.screen_name}: {t.all_text}' for t in tweets[:10]])
    output = split_2000(output)
    return output


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
