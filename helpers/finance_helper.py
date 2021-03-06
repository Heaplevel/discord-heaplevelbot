import logging

import yfinance

logger = logging.getLogger('bot_logger')
cache = {}
cache_hits, cache_miss = 0, 0


def finance_history(stock, start=None, end=None):
    ticker = get_ticker(stock)
    if start and end:
        return ticker.history(start=start, end=end)
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
    info = ticker.info
    ticker_info = [info.get('longBusinessSummary'),
                   info.get('sector'),
                   info.get('website')
                   ]

    ticker_info = '\n'.join(ticker_info)

    # Some recommendations from big companies
    recommendations = ticker.recommendations.tail(5).to_string()

    summary = '\n'.join([ticker_info, '', '### RECOMMENDATIONS ### ', recommendations])
    return summary


def finance_calendar(stock):
    ticker = get_ticker(stock)
    return ticker.calendar


def finance_plot(stock, start="2020-10-01", end="2020-10-30"):
    import matplotlib.pyplot as plt
    import tempfile

    data = finance_history(stock, start=start, end=end)

    path = tempfile.mkstemp(suffix='.png')[1]
    plt.plot(data, scalex=300, scaley=300)
    plt.xticks(fontsize=7)
    plt.title('Change label axis font size in matplotlib')
    plt.savefig(path)
    plt.close()

    return path

    # with open(path,'rb') as img:
    #    await ctx.send(file=File(img))
