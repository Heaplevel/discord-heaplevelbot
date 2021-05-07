from discord.ext import commands


class ScheduledCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command("s1")
    def s10(self, ctx):
        pass



