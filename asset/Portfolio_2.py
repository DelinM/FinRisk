import Stock as Stock


class Portfolio:

    def __init__(self):
        self.stocks = {}

    def add_stock(self, stock: Stock):
        if isinstance(stock, Stock):
            self.stocks[stock] = stock.weight
