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
    l = []

    ticker = get_ticker(stock)

    for k,v in ticker.info.items():
        l.append(':'.join([k,str(v)]))

    recommendations = ticker.recommendations.tail(5).to_string()

    ticker_info = '\n'.join(l[:3])
    summary = '\n'.join([ticker_info, '', '### RECOMMENDATIONS ### ', recommendations])
    return summary


res = finance_helper('msft')
history = finance_history('msft')
print(res)
print(history)