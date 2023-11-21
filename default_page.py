import streamlit as st
import stTools as tools


def load_page():
    st.markdown(
        """
            Welcome to :green[FinRisk]! Explore this app to assess and simulate 
            your investment portfolio's risk effortlessly! :green[Risk management] is like 
            :blue[wearing a helmet while riding a bike]—it shields your money during investments. 
            It's a strategy set to understand uncertainties in stocks or bonds.

            Imagine your investment journey as a game; knowing rules and setbacks gives you a competitive edge. 
            :green[Value at Risk (VaR)] and :green[Conditional Value at Risk (CVaR)] aid in smart risk navigation, 
            keeping your game plan robust. Don't worry, I'll explain these concepts in a bit.
            
            Build your :green[portfolio] on the sidebar; guidance is provided! Contact me at 
            [DelinM](https://www.linkedin.com/in/raymond-mu/)
            """
    )

    st.subheader(f"Market Preview")

    col_stock1, col_stock_2, col_stock_3, col_stock_4 = st.columns(4)

    with col_stock1:
        tools.create_candle_stick_plot(stock_ticker_name="^DJI",
                                       stock_name="Dow Jones Industrial")

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
