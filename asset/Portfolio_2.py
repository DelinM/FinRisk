import Stock as Stock


class Portfolio:

    def __init__(self, stocks: set) -> None:
        self.stocks = stocks

    def add_stock(self, stock: Stock) -> None:
        if isinstance(stock, Stock):
            self.stocks.add(stock)

    def