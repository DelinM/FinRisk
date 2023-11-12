import datetime
import yfinance


class Stock:

    def __init__(self, stock_name: str):
        self.stock_name = stock_name
        self.stock_ticker = yfinance.Ticker(stock_name)
        self.owned_quantity = 0
        self.previous_close = None
        self.previous_open = None
        self.previous_volume = None
        self.previous_date = None

        self.purchased_price = None
        self._update_stock()

    def __eq__(self, other):
        if self.stock_name == other.stock_name:
            return True
        return False


    def _update_stock(self) -> None:
        """
        Updates the stock information, used as a check function to check if
        stock exist
        """
        stock_info = self.stock_ticker.history(period="1d")
        if len(stock_info) == 0:
            raise Exception("Invalid stock, enter a valid stock")
        else:
            self.previous_date = stock_info.index[0]
            self.previous_open = stock_info.loc[stock_info.index[0], "Open"]
            self.previous_close = stock_info.loc[stock_info.index[0], "Close"]
            self.previous_volume = stock_info.loc[stock_info.index[0], "Volume"]

    def _update_purchase_price(self, purchase_date: datetime.datetime) -> None:
        """
        Gets the purchase price (assumed be closed price) of the stock based
        on given date if price at given date not found, track back for 5 days,
        thought: smart implementation might be required for caching
        """
        target_date = None
        day_shift = 1
        time_delta = datetime.timedelta(days=1)
        start_date = purchase_date
        end_date = purchase_date + time_delta

        for _ in range(5):
            info = self.stock_ticker.history(start=start_date, end=end_date)
            if len(info) > 0:
                self.purchased_price = info.lock[info.index[0], "Close"]
                return
            start_date = start_date - time_delta
            end_date = end_date - time_delta

        raise Exception("Purchase price not found, please check the date or stock sticker")

    def add_buy_action(self, quantity: int,
                       purchase_date: datetime.datetime) -> None:
        """
        Add a purchase to the stock. Currently, do not support to add another
        purchase to the stock
        """

        if self.owned_quantity > 0:
            raise Exception("Stock already owned, Logic for later purchase to be added")

        self.owned_quantity += quantity

        self._update_purchase_price(purchase_date=purchase_date)

    def get_book_cost(self) -> float:
        if self.owned_quantity == 0:
            raise Exception("Stock not owned, please purchase first")

        if self.purchased_price is None:
            raise Exception("Purchase price not found, please check the date or stock sticker")

        return self.purchased_price * self.owned_quantity
