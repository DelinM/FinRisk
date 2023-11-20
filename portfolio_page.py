import streamlit as st
import stTools as tools
import portfolio_page_components
import pandas as pd


def load_page():
    no_stocks = st.session_state.no_investment

    # load portfolio performance

    my_portfolio = tools.build_portfolio(no_stocks=no_stocks)
    my_portfolio.update_market_value()

    portfolio_book_amount = my_portfolio.book_amount
    portfolio_market_value = my_portfolio.market_value
    diff_amount = portfolio_market_value - portfolio_book_amount
    pct_change = (diff_amount) \
                 / portfolio_book_amount * 100

    # save my_portfolio to session state
    st.session_state.my_portfolio = my_portfolio

    # create 3 columns
    col1_summary, col2_pie = st.columns(2)

    with col1_summary:
        portfolio_page_components.load_portfolio_performance_cards(
            portfolio_book_amount=portfolio_book_amount,
            portfolio_market_value=portfolio_market_value,
            diff_amount=diff_amount,
            pct_change=pct_change
        )

    with col2_pie:
        portfolio_page_components.load_portfolio_summary_pie()

    # load portfolio summary
    portfolio_page_components.load_portfolio_summary_table()

    # load investment preview
    st.subheader("Investment Performance Summary - Since Purchase")
    portfolio_page_components.load_portfolio_preview(no_stocks=no_stocks)
