import logging

import yfinance

logger = logging.getLogger('bot_logger')
cache = {}
cache_hits, cache_miss = 0, 0


def finance_history(stock):
    ticker = get_ticker(stock)
    return ticker.history()


def get_ticker(stock):
    global cache_miss, cache_hits
    ticker = cache.get(stock, None)
    if not ticker:
        cache_miss += 1
        logger.debug(f'cache miss for ticker {stock}')
        ticker = yfinance.Ticker(stock)
        cache.setdefault(stock, ticker)
    else:
        cache_hits += 1
        logger.debug(f'cache hit for ticker {stock}')

    return cache.get(stock)


def finance_helper(stock):
    """
    General finance helper to get info about a stock
    :param stock:
    :return:
    """
    l = []

    ticker = get_ticker(stock)
    # Some basic company info
    for k, v in ticker.info.items():
        l.append(':'.join([k, str(v)]))
    ticker_info = '\n'.join(l[:3])

    # Some recommendations from big companies
    recommendations = ticker.recommendations.tail(5).to_string()

    summary = '\n'.join([ticker_info, '', '### RECOMMENDATIONS ### ', recommendations])
    return summary
