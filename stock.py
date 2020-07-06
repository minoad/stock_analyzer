import json
import time
from datetime import datetime

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
            data = self.finnhub_client.stock_symbols(
                'US')[start_index:end_index]

        symbol_list = [i.symbol for i in data]
        return symbol_list


class Stock(object):

    def __str__(self):
        return f"{self.symbol}, {self.buzz}, {self.bullish_percent}, {self.current_price}, {self.target_mean}, {self.target_diff}, {self.targetHiLowDiff}, {self.downside}"

    def __init__(self, symbol, run_id=""):
      """[summary]

      Args:
          symbol ([type]): [description]
          run_id (str, optional): run_id indicates if a run_id will be appended to the file output. Defaults to "".
      """
      self.run_id = run_id
      self.symbol = symbol
      self.finnhub_client = self._getFinnhubClient()
      self.output_file = self._getOutputFile()
      self.GetNewsSentiment()
      self.GetPriceTarget()
      self.GetPriceQuote()
      self.GetTargetDiff()
      self.GetHiLowTargetDiff()
      self.GetDownside()
      self.SaveToOutputFile()

    def SaveToOutputFile(self):
        f = open(self.output_file, "a")
        if self.run_id == "":
          f.write(f"{datetime.now()},{str(self)}\n")
        else:
          f.write(f"{self.run_id},{datetime.now()},{str(self)}\n")
        f.close()

    def _getOutputFile(self):
        with open('config/config.json') as config_file:
            output_file = json.load(config_file)["output_file"]
        return output_file

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

    def GetDownside(self):
        if (self.target_low is not None and self.current_price is not None) and self.current_price > 0 and self.target_low > 0:
            self.downside = round(self.target_low - self.current_price, 2)
        else:
            self.downside = -1.0

    def GetHiLowTargetDiff(self):
        if self.target_high > 0 and self.target_low > 0:
            self.targetHiLowDiff = round(
                abs(self.target_high - self.target_low), 2)
        else:
            self.targetHiLowDiff = -1.0

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
print(Stock("IDXX"))

stock_details = []
print("symbol, buzz, bullish%, current_price, target_mean, target_diff_from_cur, target_diff_hilow, possible_downside ")
for symbol in StockList(start_index=None, end_index=None).stock_list:
    # print(symbol)
  #f"{self.symbol}, {self.buzz}, {self.bullish_percent}, {self.current_price}, {self.target_mean}, {self.target_diff}, {self.targetHiLowDiff}, {self.downside}"
    time.sleep(1)
    stock = Stock(symbol, "0")
    # stocks that people are reporting about, are bullish on and the price is less than 40 dollars a share.
    # stock.buzz >= 1 and stock.bullish_percent >= 1 and
    if (stock.current_price is not None and stock.target_mean is not None) and (stock.current_price > 1 and stock.current_price < 40 and stock.target_mean > 0):
        print(stock)
        stock_details.append(stock)
