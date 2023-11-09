import datetime as dt
import yfinance


class Stock:

    def __init__(self, stock_name: str, quantity: int, trade_date: dt.datetime):
        """
        Assuming trade price is the closing price of the stock on the trade date
        """
        self.stock_name = stock_name
        self.quantity = quantity
        self.trade_date = trade_date
        self.trade_price = None

    def get_trade_price(self) -> None:
        yfinance.Ticker(self.stock_name).history(period="7d", interval="1d")
        return stock_data