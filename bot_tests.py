import random
import logging

import discord_bot.finance_helper as ft

logger = logging.getLogger('test_logger')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)


cache = {}

ticker = 'AAPL'

f_history = ft.finance_history(ticker)
f_ticker = ft.get_ticker(ticker)
f_info = ft.finance_helper(ticker)


def roll(dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        return

    result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
    return result

logger.info(f_info)
logger.info(f_ticker)
logger.info(f_history)
print(roll('10d6'))