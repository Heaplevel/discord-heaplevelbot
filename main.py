import locale
import logging
import os
import time
from pathlib import Path

import discord
from discord import utils
from discord.ext import commands

locale.setlocale(locale.LC_ALL, "en_US.utf8")
start_time = time.time()

logger = logging.getLogger('bot_logger')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename=f"./logs/bot_debug.log",
                         encoding='utf-8', mode='w+')

logger.addHandler(fh)

# Todo: Enable each module in modules folder by adding "modules.{filename}" into the following list.
MODULES = [
    'modules.commands',
    'modules.greetings',
    'modules.stocks',
    # 'modules.tweets'
]


class Bot(commands.AutoShardedBot):
    def __init__(self):
        super(Bot, self).__init__(
            command_prefix="$",
            case_insensitive=True,
            intents=discord.Intents.default())

        for module in MODULES:
            try:
                self.load_extension(module)
            except Exception as e:
                print(f'{module} not loaded.')
                print("_____________________")
                print(e)

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

    async def on_error(self, event_name, *args, **kwargs):
        logger.debug(f'Just another error {event_name}')

    async def on_disconnect(self):
        logger.debug(f'{self.user.name} status: Disconnected...')


Bot = Bot()
# Create "logs" folder if not exist
Path(f'{Path(__file__).parent.absolute()}/logs').mkdir(parents=True, exist_ok=True)
Bot.run(os.getenv('DISCORD_TOKEN'))
