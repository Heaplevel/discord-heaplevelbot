import random
import logging

from helpers import finance_helper as ft
from helpers.helpers import read_tweets, split_2000

logger = logging.getLogger('test_logger')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

cache = {}


def roll_test():
    def roll(dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception as e:
            return print(e)

        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        return result

    print(roll('10d6'))


def split_test():
    x = split_2000('a' * 2001)
    assert len(x) == 2
    print('SPLIT TEST SUCCESS')


def finance_test():
    ticker = 'AAPL'

    f_history = ft.finance_history(ticker)
    f_ticker = ft.get_ticker(ticker)
    f_info = ft.finance_helper(ticker)
    f_calendar = ft.finance_calendar(ticker)
    f_path = ft.finance_plot(ticker)

    logger.info(f_info)
    logger.info(f_ticker)
    logger.info(f_history)
    logger.info(f_calendar)
    logger.info(f_path)


def tweets_test():
    tweets = read_tweets('sveriges myndighet')
    assert len(tweets) > 2000
    print(tweets)


TWEET, FINANCE, SPLIT = False, False, True
if TWEET:
    tweets_test()
if FINANCE:
    finance_test()
if SPLIT:
    split_test()
