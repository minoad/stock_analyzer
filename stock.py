import json
import time

import finnhub


class StockList(object):
    def __init__(self, start_index=None, end_index=None):
        self.finnhub_client = self._getFinnhubClient()
        self.stock_list = self._getStockSymbols(start_index, end_index)

    def _getFinnhubClient(self):
        with open('config/config.json') as config_file:
            api_key = json.load(config_file)["api_key"]
        configuration = finnhub.Configuration(api_key={'token': api_key})
        finnhub_client = finnhub.DefaultApi(finnhub.ApiClient(configuration))
        return finnhub_client

    def _getStockSymbols(self, start_index, end_index):
        if start_index == None and end_index == None:
          data = self.finnhub_client.stock_symbols('US')
        else:
          data = self.finnhub_client.stock_symbols('US')[start_index:end_index]
        
        symbol_list = [i.symbol for i in data]
        return symbol_list


class Stock(object):

    def __str__(self):
        return f"{self.symbol}, {self.buzz}, {self.bullish_percent}, {self.current_price}, {self.target_mean}, {self.target_diff}"

    def __init__(self, symbol):
        self.symbol = symbol
        self.finnhub_client = self._getFinnhubClient()
        self.GetNewsSentiment()
        self.GetPriceTarget()
        self.GetPriceQuote()
        self.GetTargetDiff()

    def _getFinnhubClient(self):
        with open('config/config.json') as config_file:
            api_key = json.load(config_file)["api_key"]
        configuration = finnhub.Configuration(
            api_key={'token': api_key})
        finnhub_client = finnhub.DefaultApi(
            finnhub.ApiClient(configuration))
        return finnhub_client

    def _getByTicker(self, ticker, func):
        try:
            n = func(ticker)
        except finnhub.ApiException:
            # print(f"Unable to access {func} data for {ticker}")
            return {}
        except AttributeError:
            # print(f"Attribute error for {ticker} in {func}")
            return 0
        return n

    def GetTargetDiff(self):
        if self.target_mean > 0:
            diff = round(self.target_mean - self.current_price, 2)
            self.target_diff = diff
        else:
            self.target_diff = -1

    def GetNewsSentiment(self):
        news_sentiment = self._getByTicker(
            self.symbol, self.finnhub_client.news_sentiment)
        try:
            self.buzz = news_sentiment.buzz.buzz
        except:
            self.buzz = -1
        if self.buzz == None:
            self.buzz = -1

        try:
            self.bullish_percent = news_sentiment.sentiment.bullish_percent
        except:
            self.bullish_percent = -1

    def GetPriceTarget(self):
        n = self._getByTicker(
            self.symbol, self.finnhub_client.price_target)
        try:
            self.target_high = n.target_high
        except:
            self.target_high = -1

        try:
            self.target_low = n.target_low
        except:
            self.target_low = -1

        try:
            self.target_mean = n.target_mean
        except:
            self.target_mean = -1

        try:
            self.target_median = n.target_median
        except:
            self.target_median = -1

    def GetPriceQuote(self):
        n = self._getByTicker(self.symbol, self.finnhub_client.quote)

        try:
            self.current_price = n.c
        except:
            self.current_price = -1

        try:
            self.high_price = n.h
        except:
            self.high_price = -1

        try:
            self.low_price = n.l
        except:
            self.low_price = -1

        try:
            self.open_price = n.o
        except:
            self.open_price = -1



#stocklist = StockList(0, 100)

#n = Stock("IDXX")
# print(stocklist.stock_list)
# print(n)

stock_details = []
for symbol in StockList(start_index=None, end_index=None).stock_list:
    time.sleep(1)
    stock = Stock(symbol)
    # stocks that people are reporting about, are bullish on and the price is less than 40 dollars a share.
    if stock.buzz >= 1 and stock.bullish_percent >= 1 and stock.current_price < 40 :
        print(stock)
        stock_details.append(stock)