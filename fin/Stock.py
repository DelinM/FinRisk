import datetime as dt
import yfinance


class Stock:

    def __init__(self, stock_name: str):
        self.stock_name = stock_name
        self.previous_close = None
        self.previous_open = None
        self.previous_volumn = None
        self.previous_date = None
        self.owned_quantity = 0

        self._update_stock(self.stock_name)

    def _update_stock(self, stock_name: str) -> None:
        """
        Updates the stock information, used as a check function to check if
        stock exist
        """
        stock_ticker = yfinance.Ticker(stock_name)
        stock_info = stock_ticker.history(period="1d")
        if len(stock_info) == 0:
            raise Exception("Invalid stock, enter a valid stock")
        else:
            self.previous_date = stock_info.index[0]
            self.previous_open = stock_info.loc[stock_info.index[0], "Open"]
            self.previous_close = stock_info.loc[stock_info.index[0], "Close"]
            self.previous_volumn = stock_info.loc[stock_info.index[0], "Volume"]

    def update_stock(self) -> None:
        """
        Updates the stock information
        """
        self._update_stock(self.stock_na



#
# random_stock = Stock("AAPL")
# print(random_stock.get_preivous_close())
