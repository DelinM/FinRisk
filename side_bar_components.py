import streamlit as st
import stTools as tools
import datetime as dt
import random


def load_sidebar_dropdown_stocks(port_tab: st.sidebar.tabs) -> None:
    # add dropdown menu for portfolio
    st.session_state["no_investment"] = port_tab.selectbox("Select No. of Investments",
                                                           [2, 3, 4],
                                                           index=0,
                                                           key="side_bar_portfolio_name")


def load_sidebar_stocks(port_tab: st.sidebar.tabs, no_investment: int) -> None:
    demo_stock_list = tools.get_stock_demo_data(no_investment)

    # split into three columns
    stock_col, share_col, date_col = port_tab.columns(3)

    # create text boxes for each stocks in demo_stock_list
    for stock in demo_stock_list:
        with stock_col:
            tools.create_stock_text_input(state_variable=f"stock_{demo_stock_list.index(stock) + 1}_name",
                                          default_value=stock,
                                          present_text=f"Investment {demo_stock_list.index(stock) + 1}",
                                          key=f"side_bar_stock_{demo_stock_list.index(stock) + 1}_name")

        with share_col:
            no_shares = random.randrange(500, 3000, 500)
            tools.create_stock_text_input(state_variable=f"stock_{demo_stock_list.index(stock) + 1}_share",
                                          default_value=str(no_shares),
                                          present_text="No. of Shares",
                                          key=f"side_bar_stock_{demo_stock_list.index(stock) + 1}_share")

        with date_col:
            time_delta = dt.timedelta(days=random.randrange(3, 120, 1))
            tools.create_date_input(state_variable=f"stock_{demo_stock_list.index(stock) + 1}_purchase_date",
                                    present_text="Purchase Date",
                                    default_value=dt.datetime.now() - time_delta,
                                    key=f"side_bar_stock_{demo_stock_list.index(stock) + 1}_purchase_date")


def load_sidebar_risk_model(risk_tab: st.sidebar.tabs) -> None:
    col_monte1, col_monte2 = risk_tab.columns(2)

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
