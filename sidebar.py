import streamlit as st
import stTools as tools
import datetime as dt

def load_sidebar() -> None:
    st.sidebar.title("Portfolio Building")

    if "init_cash" not in st.session_state:
        st.session_state["init_cash"] = 100

    st.session_state["init_cash"] = \
        st.sidebar.text_input("Portfolio Initial Investment ($)",
                              key="side_bar_portfolio_init_cash",
                              value=st.session_state["init_cash"])

    # split into two columns
    stock_col, weight_col = st.sidebar.columns(2)

    with stock_col:
        # stock 1
        tools.create_stock_text_input(state_variable="stock_1_name",
                                      default_value="AAPL",
                                      present_text="Investment 1",
                                      key="side_bar_stock_1_name")
        # stock 2
        tools.create_stock_text_input(state_variable="stock_2_name",
                                      default_value="TSLA",
                                      present_text="Investment 2",
                                      key="side_bar_stock_2_name")
        # stock 3
        tools.create_stock_text_input(state_variable="stock_3_name",
                                      default_value="AMZN",
                                      present_text="Investment 3",
                                      key="side_bar_stock_3_name")
        # stock 4
        tools.create_stock_text_input(state_variable="stock_4_name",
                                      default_value="GOOG",
                                      present_text="Investment 4",
                                      key="side_bar_stock_4_name")

        # start date
        tools.create_date_input(state_variable="start_date",
                                present_text="Start Date",
                                default_value=dt.datetime.now() - dt.timedelta(days=365),
                                key="side_bar_start_date")

    with weight_col:
        # stock 1 weight percentage
        tools.create_stock_text_input(state_variable="stock_1_weight",
                                      default_value=0.5,
                                      present_text="Weight 1",
                                      key="side_bar_stock_1_weight")
        # stock 2 weight percentage
        tools.create_stock_text_input(state_variable="stock_2_weight",
                                      default_value=0.2,
                                      present_text="Weight 2",
                                      key="side_bar_stock_2_weight")
        # stock 3 weight percentage
        tools.create_stock_text_input(state_variable="stock_3_weight",
                                      default_value=0.2,
                                      present_text="Weight 3",
                                      key="side_bar_stock_3_weight")
        # stock 4 weight percentage
        tools.create_stock_text_input(state_variable="stock_4_weight",
                                      default_value=0.1,
                                      present_text="Weight 4",
                                      key="side_bar_stock_4_weight")

        # end date
        tools.create_date_input(state_variable="end_date",
                                present_text="End Date",
                                default_value=dt.datetime.now(),
                                key="side_bar_end_date")

    result = tools.click_button("load_portfolio")
    st.session_state["load_portfolio"] = st.sidebar.button("Load Portfolio",
                                                           key="side_bar_load_portfolio",
                                                           on_click=result)