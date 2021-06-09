from discord.ext import commands, tasks


class ScheduledCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.s10.start()

    @tasks.loop(hours=24, count=5)
    async def s10(self):
        channels = self.bot.get_all_channels()

        for c in channels:
            if c.name == 'bot-playground':
                print(c)
                await c.send('Sending scheduled task message')


def setup(bot):
    scheduled_commands = ScheduledCommands(bot)
    bot.add_cog(scheduled_commands)

