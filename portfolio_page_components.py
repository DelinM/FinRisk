import streamlit as st
import stTools as tools
import pandas as pd


def load_portfolio_performance_cards(
        portfolio_book_amount: float,
        portfolio_market_value: float,
        diff_amount: float,
        pct_change: float
) -> None:
    st.subheader("Portfolio Performance (with Dividends))")
    tools.create_metric_card(label="Book Cost of Portfolio",
                             value=tools.format_currency(portfolio_book_amount),
                             delta=None)
    tools.create_metric_card(label="Market Value of Portfolio",
                             value=tools.format_currency(portfolio_market_value),
                             delta=None)
    tools.create_metric_card(label="Gain/Loss on Investments Unrealized",
                             value=tools.format_currency(diff_amount),
                             delta=f"{pct_change:.2f}%")


def load_portfolio_summary_pie() -> None:
    st.subheader("Portfolio Distribution")
    book_cost_list = {}
    for stock in st.session_state.my_portfolio.stocks.values():
        book_cost_list[stock.stock_name] = stock.get_book_cost()

    # create pie chart
    tools.create_pie_chart(book_cost_list)

def load_portfolio_summary_table() -> None:
    st.subheader("Portfolio Summary")

    # for each stock, we get book cost, market value, gain/loss, and pct change
    stock_info = {}
    for stock in st.session_state.my_portfolio.stocks.values():
        # round to 2 decimal places
        book_cost = round(stock.get_book_cost(), 2)
        market_value = round(stock.get_market_value(), 2)
        gain_loss = round(market_value - book_cost, 2)
        pct_change = round((gain_loss) / book_cost * 100, 2)

        stock_info[stock.stock_name] = [book_cost, market_value, gain_loss, pct_change]
    # print key and values in stock_info
    for key, value in stock_info.items():
        print(key, value)

    column_names = ['Book Cost', 'Market Value', 'Gain/Loss', '% Change']
    stock_df = pd.DataFrame.from_dict(stock_info,
                                      orient='index',
                                      columns=column_names)
    # name index column as 'Stock'
    stock_df.index.name = 'Stock'

    for column in stock_df.columns:
        stock_df[column] = stock_df[column].apply(lambda x: f'{x:,.2f}')

    # plot dataframe stock_df
    st.dataframe(
        stock_df.style.map(tools.win_highlight,
                           subset=['Gain/Loss', '% Change']),
        column_config={
            "Stock": "Ticker",
            "Book Cost": "Book Cost($)",
            "Market Value": "Market Value($)",
            "Gain/Loss": "Gain/Loss($)",  # if positive, green, if negative, red
            "% Change": "% Change",  # if positive, green, if negative, red
        },
        hide_index=True,
        width=5600,
    )


def load_portfolio_preview(no_stocks: int) -> None:
    column_limit = 4
    # create 4 columns
    col_stock1, col_stock_2, col_stock_3, col_stock_4 = st.columns(column_limit)
    columns_list = [col_stock1, col_stock_2, col_stock_3, col_stock_4]

    columns_no = 0
    for i in range(no_stocks):
        if columns_no == 4:
            columns_no = 0
        with columns_list[columns_no]:
            tools.preview_stock(f"stock_{i + 1}_name",
                                start_date=st.session_state[f"stock_{i + 1}_purchase_date"])
        columns_no += 1
