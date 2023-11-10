import datetime as dt
import yfinance


class Stock:

    def __init__(self, stock_name: str):

        self.stock_name = stock_name
        Stock._validate_stock(stock_name)
        self.trade_price = None

    @staticmethod
    def _validate_refresh_stock(stock_name: str):
        stock_ticker = yfinance.Ticker(stock_name)
        stock_info = stock_ticker.history(period="1d")
        if len(stock_info) == 0:
            raise Exception("Invalid stock, enter a valid stock")
        else:




random_stock = Stock("AAPL")
