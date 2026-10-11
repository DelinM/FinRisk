import yfinance
import pandas as pd
import datetime

# Yahoo Finance rejects the plain `requests` client that older yfinance used.
# Current yfinance impersonates a browser via curl_cffi; without it, downloads
# come back empty or blocked.
try:
    import curl_cffi  # noqa: F401
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "curl_cffi is required. Yahoo Finance blocks yfinance unless the "
        "client impersonates a browser. Install it with: pip install curl_cffi"
    ) from exc


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
        # Current yfinance raises if period is sent together with start and end.
        if start is not None or end is not None:
            return ticker.history(interval=interval, start=start, end=end)
        return ticker.history(period=period, interval=interval)

    @staticmethod
    def get_demo_daily_history(interval: str):
        # use apple's last tuesday (from today) data as demo
        today = datetime.datetime.today()
        last_tuesday = today - datetime.timedelta(days=(today.weekday() - 1) % 7)
        next_day = last_tuesday + datetime.timedelta(days=1)
        return InfoCollector.get_history(
            ticker=yfinance.Ticker("AAPL"),
            period="1d",
            interval=interval,
            start=last_tuesday.strftime("%Y-%m-%d"),
            end=next_day.strftime("%Y-%m-%d"))

    @staticmethod
    def get_prev_date(stock_info: pd.DataFrame):
        return stock_info.index[0]

    @staticmethod
    def get_daily_info(stock_info: pd.DataFrame, key_info: str):
        return stock_info.loc[stock_info.index[0], key_info]

    @staticmethod
    def download_history(stocks, start_time, end_time, multi_level_index: bool = True):
        """
        Download daily OHLC. auto_adjust stays False so Close matches the
        unadjusted closes this app used with yfinance 0.2.x.

        A single ticker needs multi_level_index=False. Otherwise Close is a
        MultiIndex column and callers that expect a scalar price break.
        """
        return yfinance.download(
            stocks,
            start=start_time,
            end=end_time,
            auto_adjust=False,
            progress=False,
            multi_level_index=multi_level_index,
        )

    @staticmethod
    def download_batch_history(stocks: list, start_time, end_time):
        return InfoCollector.download_history(stocks, start_time, end_time)