from assets.Collector import InfoCollector
from assets.Stock import Stock

class Portfolio:

    def __init__(self) -> None:
        self.stocks = {}
        self.book_amount = 0
        self.market_value = 0

    def add_stock(self, stock: Stock) -> None:
        if stock.stock_name in self.stocks.keys():
            raise Exception("Stock included in portfolio. Please remove stock to add again")

        self.stocks[stock.stock_name] = stock
        self.book_amount += stock.get_book_cost()

    def remove_stock(self, stock_name: str) -> None:
        if stock_name not in self.stocks.keys():
            raise Exception("Stock not in portfolio")
        self.book_amount -= self.stocks[stock_name].get_book_cost()
        self.stocks.pop(stock_name)

    def update_market_value(self) -> None:
        for stock in self.stocks.values():
            stock_history = InfoCollector.get_history(stock.ticker, period="1d")
            stock_price = InfoCollector.get_daily_info(stock_history, "Close")
            self.market_value += stock_price * stock.average_price
