import streamlit as st
import stTools as tools



def load_portfolio_preview(no_stocks: int) -> None:
    # create 4 columns
    col_stock1, col_stock_2, col_stock_3, col_stock_4 = st.columns(4)
    columns_list = [col_stock1, col_stock_2, col_stock_3, col_stock_4]

    for i in range(no_stocks):
        with columns_list[i]:
            tools.preview_stock(f"stock_{i + 1}_name",
                                start_date=st.session_state[f"stock_{i + 1}_purchase_date"])
