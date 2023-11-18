import streamlit as st
import stTools as tools


def load_default_page():
    st.subheader(f"Market Preview")

    col_stock1, col_stock_2, col_stock_3, col_stock_4 = st.columns(4)

    with col_stock1:
        tools.create_candle_stick_plot(stock_ticker_name="^DJI",
                                       stock_name="Dow Jones Industrial Average")

    with col_stock_2:
        tools.create_candle_stick_plot(stock_ticker_name="^IXIC",
                                       stock_name="Nasdaq Composite")

    with col_stock_3:
        tools.create_candle_stick_plot(stock_ticker_name="^GSPC",
                                       stock_name="S&P 500")

    with col_stock_4:
        tools.create_candle_stick_plot(stock_ticker_name="^RUT",
                                       stock_name="Russell 2000")

    # make 2 columns for sectors
    col_sector1, col_sector2 = st.columns(2)

    with col_sector1:
        st.subheader(f"Tech Stocks")
        stock_list = ["AAPL", "MSFT", "AMZN", "GOOG", "META", "TSLA", "NVDA", "AVGO"]
        stock_name = ["Apple", "Microsoft", "Amazon", "Google", "Meta", "Tesla", "Nvidia", "Broadcom"]

        df_stocks = tools.create_stocks_dataframe(stock_list, stock_name)
        tools.create_dateframe_view(df_stocks)

    with col_sector2:
        st.subheader(f"Meme Stocks")
        # give me a list of 8 meme stocks
        stock_list = ["GME", "AMC", "BB", "NOK", "RIVN", "SPCE", "F", "T"]
        stock_name = ["GameStop", "AMC Entertainment", "BlackBerry", "Nokia", "Rivian",
                      "Virgin Galactic", "Ford", "AT&T"]

        df_stocks = tools.create_stocks_dataframe(stock_list, stock_name)
        tools.create_dateframe_view(df_stocks)
