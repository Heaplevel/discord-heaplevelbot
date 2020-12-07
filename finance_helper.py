import yfinance

cache = {}


def finance_history(stock):
    ticker = get_ticker(stock)
    return ticker.history()


def get_ticker(stock):
    ticker = cache.get(stock, None)
    if not ticker:
        ticker = yfinance.Ticker(stock)
        cache.setdefault(stock, ticker)
    return cache.get(stock)


def finance_helper(stock):
    """
    General finance helper to get info about a stock
    :param stock:
    :return:
    """
    l = []

    ticker = cache.get(stock, None)
    if not ticker:
        ticker = yfinance.Ticker(stock)
        cache.setdefault(stock, ticker)

    for k, v in ticker.info.items():
        l.append(':'.join([k, str(v)]))

    recommendations = ticker.recommendations.tail(5).to_string()

    ticker_info = '\n'.join(l[:3])
    summary = '\n'.join([ticker_info, '', '### RECOMMENDATIONS ### ', recommendations])
    return summary
