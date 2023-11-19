import streamlit as st
import stTools as tools
import datetime as dt


def load_sidebar_dropdown_stocks(port_tab: st.sidebar.tabs) -> None:
    # add dropdown menu for portfolio
    st.session_state["no_investment"] = port_tab.selectbox("Select No. of Investments",
                                                             [2, 3, 4],
                                                             index=2,
                                                             key="side_bar_portfolio_name")


def load_sidebar_stocks(port_tab: st.sidebar.tabs, no_investment: int) -> None:
    pass


def load_sidebar_risk_model(risk_tab: st.sidebar.tabs) -> None:

    risk_tab.title("Risk Model Building")

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

    st.session_state["run_simulation"] = risk_tab.button("Run Simulation",
                                                         key="main_page_run_simulation",
                                                         on_click=tools.click_button_sim)
