import yfinance
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

from numpy import ndarray


class Portfolio:

    def __init__(self, init_cash: float, start_date, end_date):
        self.cVaR_alpha = None
        self.VaR_alpha = None
        self.portfolio_returns = None
        self.init_cash = init_cash
        self.total_weight = 1
        self.stocks = {}
        self.start_time = start_date
        self.end_time = end_date
        self.pct_return = None
        self.pct_mean_return = None
        self.pct_cov_matrix = None
        self.VaR = None
        self.cVaR = None

        if start_date > end_date:
            raise Exception("Start time is greater than end time")

    def _validate_stock(self, stock: str) -> bool:
        info = yfinance.Ticker(stock).history(period="7d", interval="1d")
        return len(info) > 0

    def add_stock(self, stock: str, weight: float):
        if round(self.total_weight, 1) < weight:
            raise Exception(f"Weight is too large, available weight: {self.total_weight}, "
                            f"provided weight: {weight})")

        if stock in self.stocks:
            raise Exception("Stock already exists, enter a new stock")

        if self._validate_stock(stock):
            self.stocks[stock] = weight
            self.total_weight -= weight
        else:
            raise Exception("Invalid stock, enter a valid stock")

    def remove_stock(self, stock: str) -> None:
        if stock not in self.stocks:
            raise Exception("Stock does not exist, enter a valid stock")

        self.total_weight += self.stocks[stock]
        del self.stocks[stock]

    def get_portfolio_history(self) -> None:
        stocks = list(self.stocks.keys())
        stocks_data = yfinance.download(stocks, start=self.start_time, end=self.end_time)

        # Get the closing price of each stock apply dropna()
        stocks_data = stocks_data['Close'].dropna()

        self.pct_return = stocks_data.pct_change().dropna()
        self.pct_mean_return = self.pct_return.mean()
        self.pct_cov_matrix = self.pct_return.cov()

    def apply_monte_carlo(self, no_simulations: int, no_days: int) -> None:
        # Get weight array
        weights = list(self.stocks.values())
        weights = np.array(weights, dtype=np.float64)

        # get mean matrix
        mean_matrix = np.full(shape=(no_days, len(weights)), fill_value=self.pct_mean_return)
        mean_matrix = np.transpose(mean_matrix)

        portfolio_returns = np.zeros(shape=(no_days, no_simulations), dtype=np.float64)

        for sim in range(0, no_simulations):
            # Cholesky Decomposition
            Z = np.random.normal(size=(no_days, len(weights)))
            L = np.linalg.cholesky(self.pct_cov_matrix)

            daily_returns = mean_matrix + np.inner(L, Z)
            portfolio_returns[:, sim] = np.cumprod(np.inner(weights, daily_returns.T) + 1) \
                                        * self.init_cash
        self.portfolio_returns = portfolio_returns

    def plot_monte_carlo(self):

        plt.figure(figsize=(12, 8))
        plt.plot(self.portfolio_returns)
        plt.ylabel('Portfolio Value ($)', fontsize=12)
        plt.xlabel('Days', fontsize=12)


        # if self.VaR  and self.cVaR exist, plot them on chart
        if self.VaR and self.cVaR:
            plt.axhline(y=self.VaR, color='r', linestyle=':', linewidth=4, label=f'VaR: {self.VaR}')
            plt.axhline(y=self.cVaR, color='g', linestyle=':', linewidth=4, label=f'cVaR: {self.cVaR}')
            plt.legend(loc='upper left', fontsize=12)
            print(self.VaR_alpha)
            plt.title(f'Portfolio Performance with VaR(alpha={self.VaR_alpha}) '
                      f'& cVaR(alpha={self.cVaR_alpha})', fontsize=15)
        plt.margins(0.02)
        plt.show()

    def get_VaR(self, alpha: float) -> int:
        if self.VaR_alpha is None:
            self.VaR_alpha = alpha
        if self.portfolio_returns is None:
            raise Exception("No Monte Carlo simulation has been applied")

        self.VaR = round(np.quantile(self.portfolio_returns[-1, :], self.VaR_alpha), 1)
        return self.VaR

    def get_conditional_VaR(self, alpha: float) -> ndarray:
        self.cVaR_alpha = alpha
        if self.portfolio_returns is None:
            raise Exception("No Monte Carlo simulation has been applied")

        var = self.get_VaR(self.cVaR_alpha)
        self.cVaR = round(np.mean(self.portfolio_returns[-1, :][self.portfolio_returns[-1, :] < var]),1)
        return self.cVaR