import streamlit as st
import stTools as tools
import portfolio_page_components


def load_page():

    no_stocks = st.session_state.no_investment

    # load investment preview
    st.subheader("Investment Performance Summary")
    portfolio_page_components.load_portfolio_preview(no_stocks=no_stocks)

    # load portfolio performance
    st.subheader("Portfolio Performance")

    my_portfolio = tools.build_portfolio(no_stocks=no_stocks)

    

