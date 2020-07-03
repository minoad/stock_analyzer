import time

import finnhub

# Configure API key
configuration = finnhub.Configuration(
    api_key={
        'token': 'brv3prnrh5r9k3fgq72g'  # Replace this
    }
)

finnhub_client = finnhub.DefaultApi(finnhub.ApiClient(configuration))

# Stock candles
# print(finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249))

# Aggregate Indicators
# print(finnhub_client.aggregate_indicator('AAPL', 'D'))

# # Basic financials
# print(finnhub_client.company_basic_financials('AAPL', 'margin'))

# # Earnings surprises
# print(finnhub_client.company_earnings('TSLA', limit=5))

# # EPS estimates
# print(finnhub_client.company_eps_estimates('AMZN', freq='quarterly'))

# # Company Executives
# print(finnhub_client.company_executive('AAPL'))

# # Company News
# # Need to use _from instead of from to avoid conflict
# print(finnhub_client.company_news('AAPL', _from="2020-06-01", to="2020-06-10"))

# # Company Peers
# print(finnhub_client.company_peers('AAPL'))

# # Company Profile
# print(finnhub_client.company_profile(symbol='AAPL'))
# print(finnhub_client.company_profile(isin='US0378331005'))
# print(finnhub_client.company_profile(cusip='037833100'))

# # Company Profile 2
# print(finnhub_client.company_profile2(symbol='AAPL'))

# # Revenue Estimates
# print(finnhub_client.company_revenue_estimates('TSLA', freq='quarterly'))

# # List country
# print(finnhub_client.country())

# # Crypto Exchange
# print(finnhub_client.crypto_exchanges())

# # Crypto symbols
# print(finnhub_client.crypto_symbols('BINANCE'))

# # Economic data
# print(finnhub_client.economic_data('MA-USA-656880'))

# # Filings
# print(finnhub_client.filings(symbol='AAPL', _from="2020-01-01", to="2020-06-11"))

# # Financials
# print(finnhub_client.financials('AAPL', 'bs', 'annual'))

# # Financials as reported
# print(finnhub_client.financials_reported(symbol='AAPL', freq='annual'))

# # Forex exchanges
# print(finnhub_client.forex_exchanges())

# # Forex all pairs
# print(finnhub_client.forex_rates(base='USD'))

# # Forex symbols
# print(finnhub_client.forex_symbols('OANDA'))

# # Fund Ownership
# print(finnhub_client.fund_ownership('AMZN', limit=5))

# # General news
# print(finnhub_client.general_news('forex', min_id=0))

# # Investors ownership
# print(finnhub_client.investors_ownership('AAPL', limit=5))

# # IPO calendar
# print(finnhub_client.ipo_calendar(_from="2020-05-01", to="2020-06-01"))

# # Major developments
# print(finnhub_client.major_developments('AAPL', _from="2020-01-01", to="2020-12-31"))


# # Recommendation trends
# print(finnhub_client.recommendation_trends('AAPL'))

# # Stock dividends
# print(finnhub_client.stock_dividends('KO', _from='2019-01-01', to='2020-01-01'))


# # Transcripts
# print(finnhub_client.transcripts('AAPL_162777'))

# # Transcripts list
# print(finnhub_client.transcripts_list('AAPL'))

# # Earnings Calendar
# print(finnhub_client.earnings_calendar(_from="2020-06-10", to="2020-06-30", symbol="", international=False))

# # Covid-19
# print(finnhub_client.covid19())

# # Upgrade downgrade
# print(finnhub_client.upgrade_downgrade(symbol='AAPL', _from='2020-01-01', to='2020-06-30'))

# # Economic code
# print(finnhub_client.economic_code()[0:5])

# # Support resistance
# print(finnhub_client.support_resistance('AAPL', 'D'))

# # Technical Indicator
# print(finnhub_client.technical_indicator(symbol="AAPL", resolution='D', _from=1583098857, to=1584308457, indicator='rsi', indicator_fields={"timeperiod": 3}))

# # Stock splits
# print(finnhub_client.stock_splits('AAPL', _from='2000-01-01', to='2020-01-01'))

# # Forex candles
# print(finnhub_client.forex_candles('OANDA:EUR_USD', 'D', 1590988249, 1591852249))

# # Crypto Candles
# print(finnhub_client.crypto_candles('BINANCE:BTCUSDT', 'D', 1590988249, 1591852249))

# # Tick Data
# print(finnhub_client.stock_tick('AAPL', '2020-03-25', 500, 0))


# # Pattern recognition
# print(finnhub_client.pattern_recognition('AAPL', 'D'))


# Base Function.
def GetByTicker(ticker, func):
    """Gets anything by the ticker and func name

    Args:
        ticker (string): ticker string
        func (func): function to call

    Returns:
        dict of requested data or empty dict if ApiException
    """
    try:
        n = func(ticker)
    except finnhub.ApiException:
        #print(f"Unable to access {func} data for {ticker}")
        return {}
    except AttributeError:
        #print(f"Attribute error for {ticker} in {func}")
        return 0
    return n


def GetStockSymbols(start_index, end_index):
    data = finnhub_client.stock_symbols('US')[start_index:end_index]
    symbol_list = [i.symbol for i in data]
    return symbol_list


# Functions returning full details.  These functions will be called by other functions in order to parse the data.
def GetNewsSentiment(ticker="PYPL"):
    return GetByTicker(ticker, finnhub_client.news_sentiment)


def GetPriceTarget(ticker="PYPL"):
    return GetByTicker(ticker, finnhub_client.price_target)


def GetPriceQuote(ticker="PYPL"):
    return GetByTicker(ticker, finnhub_client.quote)

# Functions pulling out details


def GetBullishPercent(ticker):
    try:
        n = GetNewsSentiment(ticker).sentiment.bullish_percent
    except AttributeError:
        #print(f"Attribute error access bearish percent for {ticker}")
        return -1.0
    return n


def GetBuzzPercent(ticker):
    """
      This generates a floating point number which is avg number of articles / this week count of articles.
    Args:
        ticker ([type]): [description]

    Returns:
        [type]: [description]
    """
    try:
        n = GetNewsSentiment(ticker).buzz.buzz
    except AttributeError:
        #print(f"Attribute error access bearish percent for {ticker}")
        return -1.0
    if n == None:
        n = -1.0
    return n


def GetPriceTargetMean(ticker):
    try:
        n = GetPriceTarget(ticker).target_mean
    except AttributeError:
        #print(f"Attribute error access bearish percent for {ticker}")
        return -1.0
    return n


def GetCurrentPrice(ticker):
    try:
        n = GetPriceQuote(ticker).c
    except AttributeError:
        #print(f"Attribute error access bearish percent for {ticker}")
        return -1.0
    return n


def GetPriceDiff(ticker):
    price_target_mean = GetPriceTargetMean(ticker)
    current_price = GetCurrentPrice(ticker)
    if price_target_mean < 0 or current_price < 0:
        return -1.0
    return round(price_target_mean - current_price, 2)


symbols = GetStockSymbols(5, 100)
GetByTicker("PYPL", finnhub_client.quote)
for symbol in symbols:
    time.sleep(2)
    # print(GetNewsSentiment(symbol))
    bullish = GetBullishPercent(symbol)
    buzz = GetBuzzPercent(symbol)
    price_target_mean = GetPriceTargetMean(symbol)
    current_price = GetCurrentPrice(symbol)
    price_diff = GetPriceDiff(symbol)
    # print(GetPriceTarget(symbol))
    # print(GetPriceQuote(symbol))
    print(f"{symbol}, {bullish}, {buzz}, {current_price}, {price_target_mean}, {price_diff}")
# can i pass the names of the methods?
# print(GetBullishPercent("pypl"))
