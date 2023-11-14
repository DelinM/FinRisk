import datetime as dt
import numpy as np
from numpy import ndarray
from assets import Portfolio
from assets.Collector import InfoCollector


class Monte_Carlo_Simulator:

    def __init__(self,
                 cVaR_alpha: float,
                 VaR_alpha: float):
        self.stocks = {}
        self.init_cash = 0
        self.no_simulations = 0
        self.no_days = 0
        self.cVaR_alpha = cVaR_alpha
        self.VaR_alpha = VaR_alpha
        self.pct_mean_return = None
        self.pct_cov_matrix = None
        self.portfolio_returns = None

    def get_portfolio(self, portfolio: Portfolio,
                      start_time: dt.datetime,
                      end_time: dt.datetime) -> None:
        stocks = list(portfolio.stocks.keys())
        stocks_data = InfoCollector.download_batch_history(stocks, start_time, end_time)

        # Get the closing price of each stock apply dropna()
        stocks_data = stocks_data['Close'].dropna()

        pct_return = stocks_data.pct_change().dropna()
        self.pct_mean_return = pct_return.mean()
        self.pct_cov_matrix = pct_return.cov()

        self.init_cash = portfolio.book_amount
        self._get_weights(portfolio)

    def _get_weights(self, portfolio: Portfolio):
        total_book_cost = 0
        for stock in portfolio.stocks.keys():
            self.stocks[stock] = portfolio.stocks[stock].get_book_cost()
            total_book_cost += self.stocks[stock]

        for stock in portfolio.stocks.keys():
            self.stocks[stock] = self.stocks[stock] / total_book_cost

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

    def get_VaR(self, alpha: float) -> int:
        if self.VaR_alpha is None:
            self.VaR_alpha = float(alpha)
        if self.portfolio_returns is None:
            raise Exception("No Monte Carlo simulation has been applied")

        VaR = round(np.quantile(self.portfolio_returns[-1, :], float(self.VaR_alpha)), 1)
        return VaR

    def get_conditional_VaR(self, alpha: float) -> ndarray:
        self.cVaR_alpha = float(alpha)
        if self.portfolio_returns is None:
            raise Exception("No Monte Carlo simulation has been applied")

        var = self.get_VaR(self.cVaR_alpha)
        cVaR = round(np.mean(self.portfolio_returns[-1, :]
                                  [self.portfolio_returns[-1, :] < float(var)]),1)
        return cVaR