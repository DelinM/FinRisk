import yfinance
import pandas as pd


class InfoCollector:

    @staticmethod
    def get_ticker(stock_name: str) -> yfinance.Ticker:
        return yfinance.Ticker(stock_name)

    @staticmethod
    def get_history(ticker: yfinance.Ticker,
                    period="1mo", interval="1d",
                    start=None, end=None):
        """
         period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
        start: str
            Download start date string (YYYY-MM-DD) or _datetime, inclusive.
            Default is 99 years ago
            E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
        end: str
            Download end date string (YYYY-MM-DD) or _datetime, exclusive.
            Default is now
            E.g. for end="2023-01-01", the last data point will be on "2022-12-31"
        """
        return ticker.history(period=period, interval=interval,
                              start=start, end=end)

    @staticmethod
    def get_demo_daily_history(interval: str):
        return InfoCollector.get_history(
            ticker=yfinance.Ticker("AAPL"),
            period="1d",
            interval=interval,
            start="2023-11-15",
            end="2023-11-16")

    @staticmethod
    def get_prev_date(stock_info: pd.DataFrame):
        return stock_info.index[0]

    @staticmethod
    def get_daily_info(stock_info: pd.DataFrame, key_info: str):
        return stock_info.loc[stock_info.index[0], key_info]

    @staticmethod
    def download_batch_history(stocks: list, start_time, end_time):
        return yfinance.download(stocks, start=start_time, end=end_time)
