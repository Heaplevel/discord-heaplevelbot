#import locale
import logging
import os, sys
import time
from pathlib import Path

import discord
from discord import utils
from discord.ext import commands

#locale.setlocale(locale.LC_ALL, "en_US.utf8")
start_time = time.time()

logger = logging.getLogger('bot_logger')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename=f"./logs/bot_debug.log",
                         encoding='utf-8', mode='w+')

logger.addHandler(fh)

MODULES = [
    'modules.commands',
    'modules.greetings',
    'modules.stocks',
    'modules.tweets',
    'modules.scheduled_commands'
]


class Bot(commands.AutoShardedBot):
    def __init__(self):

        super(Bot, self).__init__(
            command_prefix="$",
            case_insensitive=True,
            intents=discord.Intents(messages=True, members=True, reactions=True, guilds=True))

        for module in MODULES:
            try:
                self.load_extension(module)
            except Exception as e:
                print(f'{module} not loaded.')
                print("_____________________")
                print(e)

    async def on_connect(self):
        logger.debug('Starting route to connect...')

    async def on_ready(self):
        """Output after the Bot fully loaded"""
        end_time = time.time() - start_time
        await self.change_presence(status=discord.Status.online)
        start_info = f'''#-------------------------------#
                            | Username: {self.user.name}
                            | User ID: {self.user.id}
                            | Developer:  HeapLevel
                            | Guilds: {len(self.guilds)}
                            | Emojis: {len(self.emojis)}
                            | Users: {len([member for member in self.users if not member.bot])}
                            | Base OAuth URL: {utils.oauth_url(self.user.id)}
                            | Bot started in {"%.3f" % end_time} seconds
                            | Current Discord.py Version: {discord.__version__}
                        # ------------------------------#'''

        logger.debug(start_info)
        print(start_info)

    async def on_typing(self, channel, user, when):
        logger.debug(f'Someone is typing in {channel}, {user}, {when}')

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        logger.debug(f'A member was updated {before.nick}, {after.nick}')


    async def on_message(self, message: discord.Message):
        guild: discord.Guild
        for guild in self.guilds:
            for channel in guild.channels:
                print(f'{channel.name}')

        ctx :discord.ext.commands.Context = await self.get_context(message)
        if ctx.valid:
            logger.debug(f'Context is valid, yes go on')
            await ctx.send(f'Content is valid...')
        else:
            logger.debug('Sorry m8 no context is valid here')


        logger.debug(f'What is this message here: {message.content} \n'
                     f'These are the channels: {[channel for channel in self.get_all_members()]}')

    async def on_error(self, event_name, *args, **kwargs):
        logger.debug(f'[Bot.Client] Just another error {event_name} \n'
                     f'{sys.exc_info()}')

    async def on_disconnect(self):
        logger.debug(f'{self.user.name} status: Disconnected...')


intents = discord.Intents.default()
intents.members = True
Bot = Bot()
# Create "logs" folder if not exist
Path(f'{Path(__file__).parent.absolute()}/logs').mkdir(parents=True, exist_ok=True)
Bot.run(os.getenv('DISCORD_TOKEN'))
