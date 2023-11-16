import streamlit as st
import stTools as tools
import datetime as dt
import random


def load_sidebar() -> None:
    # inject custom CSS to set the width of the sidebar
    tools.create_side_bar_width()

    st.sidebar.title("Control Panel")


    if "load_portfolio" not in st.session_state:
        st.session_state["load_portfolio"] = False

    if "run_simulation" not in st.session_state:
        st.session_state["run_simulation"] = False

    portfo_tab, model_tab = st.sidebar.tabs(["📈 Create Portfolio", "🐂 Build Risk Model"])

    portfo_tab.title("Portfolio Building")

    # split into three columns
    stock_col, share_col, date_col = portfo_tab.columns(3)

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

    with share_col:
        # stock 1 shares
        tools.create_stock_text_input(state_variable="stock_1_share",
                                      default_value=str(1000),
                                      present_text="No. of Shares",
                                      key="side_bar_stock_1_share")
        # stock 2 shares
        tools.create_stock_text_input(state_variable="stock_2_share",
                                      default_value=str(2000),
                                      present_text="No. of Shares",
                                      key="side_bar_stock_2_share")
        # stock 3 shares
        tools.create_stock_text_input(state_variable="stock_3_share",
                                      default_value=str(3000),
                                      present_text="No. of Shares",
                                      key="side_bar_stock_3_share")
        # stock 4 shares
        tools.create_stock_text_input(state_variable="stock_4_share",
                                      default_value=str(500),
                                      present_text="No. of Shares",
                                      key="side_bar_stock_4_share")

    with date_col:
        # stock 1 purchase date
        tools.create_date_input(state_variable="stock_1_purchase_date",
                                present_text="Purchase Date",
                                default_value=dt.datetime.now() - dt.timedelta(days=random.randint(50,100)),
                                key="side_bar_stock_1_purchase_date")
        # stock 2 purchase date
        tools.create_date_input(state_variable="stock_2_purchase_date",
                                present_text="Purchase Date",
                                default_value=dt.datetime.now() - dt.timedelta(days=random.randint(50,100)),
                                key="side_bar_stock_2_purchase_date")
        # stock 3 purchase date
        tools.create_date_input(state_variable="stock_3_purchase_date",
                                present_text="Purchase Date",
                                default_value=dt.datetime.now() - dt.timedelta(days=random.randint(50,100)),
                                key="side_bar_stock_3_purchase_date")
        # stock 4 purchase date
        tools.create_date_input(state_variable="stock_4_purchase_date",
                                present_text="Purchase Date",
                                default_value=dt.datetime.now() - dt.timedelta(days=random.randint(50,100)),
                                key="side_bar_stock_4_purchase_date")

    st.session_state["load_portfolio"] = portfo_tab.button("Load Portfolio",
                                                           key="side_bar_load_portfolio",
                                                           on_click=tools.click_button_port)

    model_tab.title("Risk Model Building")

    col_monte1, col_monte2 = model_tab.columns(2)

    with col_monte1:

        tools.create_date_input(state_variable="start_date",
                                present_text="History Start Date",
                                default_value=dt.datetime.now() - dt.timedelta(days=365),
                                key="side_bar_start_date")

        tools.create_stock_text_input(state_variable="no_simulations",
                                      default_value=str(100),
                                      present_text="No. of Simulations",
                                      key="main_no_simulations")

        tools.create_stock_text_input(state_variable="VaR_alpha",
                                      default_value=str(0.05),
                                      present_text="VaR Alpha",
                                      key="side_bar_VaR_alpha")
    with col_monte2:

        tools.create_date_input(state_variable="end_date",
                                present_text="History End Date",
                                default_value=dt.datetime.now(),
                                key="side_bar_end_date")

        tools.create_stock_text_input(state_variable="no_days",
                                      default_value=str(100),
                                      present_text="No. of Days",
                                      key="main_no_days")

        tools.create_stock_text_input(state_variable="cVaR_alpha",
                                      default_value=str(0.05),
                                      present_text="cVaR Alpha",
                                      key="side_bar_cVaR_alpha")

    st.session_state["run_simulation"] = model_tab.button("Run Simulation",
                                                           key="main_page_run_simulation",
                                                           on_click=tools.click_button_sim)
