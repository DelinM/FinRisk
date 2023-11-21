import datetime
from assets.Collector import InfoCollector


class Stock:

    def __init__(self, stock_name: str):
        self.stock_name = stock_name
        self.ticker = InfoCollector.get_ticker(stock_name)
        self.owned_quantity = 0
        self.average_price = 0
        self.previous_close = None
        self.previous_open = None
        self.previous_volume = None
        self.previous_date = None

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
        stock_info = InfoCollector.get_history(self.ticker, period="1d")
        if len(stock_info) == 0:
            raise Exception("Invalid stock, enter a valid stock")
        else:
            self.previous_date = InfoCollector.get_prev_date(stock_info)
            self.previous_open = InfoCollector.get_daily_info(stock_info, "Open")
            self.previous_close = InfoCollector.get_daily_info(stock_info, "Close")
            self.previous_volume = InfoCollector.get_daily_info(stock_info, "Volume")

    def _get_purchase_price(self, purchase_date: datetime.datetime) -> float:
        """
        Gets the purchase price (assumed be closed price) of the stock based
        on given date if price at given date not found, track back for 5 days,
        thought: smart implementation might be required for caching
        """
        time_delta = datetime.timedelta(days=1)
        start_date = purchase_date
        end_date = purchase_date + time_delta

        for _ in range(5):
            info = InfoCollector.get_history(self.ticker,
                                             start=start_date,
                                             end=end_date)
            if len(info) > 0:
                purchased_price = InfoCollector.get_daily_info(info, "Close")
                return purchased_price
            start_date = start_date - time_delta
            end_date = end_date - time_delta

        raise Exception("Purchase price not found, please check the date or stock sticker")

    def add_buy_action(self, quantity: int,
                       purchase_date: datetime.datetime) -> None:
        """
        Add a purchase to the stock. Currently, do not support to add another
        purchase to the stock
        """

        # update own quantity

        self.owned_quantity += quantity

        if self.average_price == 0:

            self.average_price = self._get_purchase_price(purchase_date=purchase_date)
        else:
            cur_purchase_price = self._get_purchase_price(purchase_date=purchase_date)
            purchase_cost = quantity * cur_purchase_price

            # update average price and owned_quantity
            total_cost = purchase_cost + cur_purchase_price
            self.average_price = total_cost / self.owned_quantity

    def get_book_cost(self) -> float:
        if self.owned_quantity == 0:
            raise Exception("Stock not owned, please purchase first")

        if self.average_price is None:
            raise Exception("Purchase price not found, please check the date or stock sticker")

        return self.average_price * self.owned_quantity

    def get_market_value(self) -> float:
        self._update_stock()
        if self.owned_quantity == 0:
            raise Exception("Stock not owned, please purchase first")

        if self.previous_close is None:
            raise Exception("Stock price not found, please check the date or stock sticker")

        return self.previous_close * self.owned_quantity

    def get_gain_loss(self) -> float:
        return self.get_market_value() - self.get_book_cost()

    def get_pct_change(self) -> float:
        return (self.get_gain_loss() / self.get_book_cost()) * 100