import streamlit as st
import pandas as pd
import stTools as tools


def add_portfolio_returns_graphs(portfolio_df: pd.DataFrame) -> None:
    tools.create_line_chart(portfolio_df)
    # st.line_chart(portfolio_df, use_container_width=True, height=500, width=250)


def add_download_button(df: pd.DataFrame) -> None:
    # convert my_portfolio_returns ndarray to dataframe
    df = pd.DataFrame(df)

    col1, col2, col3, col4 = st.columns(4)

    with col4:
        st.download_button(label="Download Portfolio Returns",
                           data=df.to_csv(),
                           file_name="Portfolio Returns.csv",
                           mime="text/csv")


def add_markdown() -> None:
    st.markdown(
        """
  Please see below for your portfolio returns after risk simulation! 
  
  Caring about :green[risk management], :green[VaR], :green[CVaR], and :green[alpha] is like 
  putting on your gaming headset—it helps you play the investment game smarter, 
  protecting your money and aiming for a high score in the financial world.
  """
    )
