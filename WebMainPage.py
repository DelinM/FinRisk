import streamlit as st
import sidebar as comp
import stTools as tools
import datetime as dt

st.set_page_config(
    page_title="FinRisk",
    page_icon="🚀",
    layout="wide"
)

st.title("Financial Risk Management Simulation - FinRisk")

comp.load_sidebar()


if "run_simulation" not in st.session_state:
    st.session_state["run_simulation"] = False

if not st.session_state["run_simulation"]:

    if not st.session_state.load_portfolio:
        st.text("Please load portfolio")

    else:
        st.subheader("Portfolio Preview")

        # create 4 columns
        col_stock1, col_stock_2, col_stock_3, col_stock_4 = st.columns(4)

        with col_stock1:
            tools.preview_stock("stock_1_name")

        with col_stock_2:
            tools.preview_stock("stock_2_name")

        with col_stock_3:
            tools.preview_stock("stock_3_name")

        with col_stock_4:
            tools.preview_stock("stock_4_name")

        st.subheader("Monte Carlo Simulation")

        # create 4 columns
        col_VaRAlpha, col_cVaRAlpha = st.columns(2)

        with col_VaRAlpha:
            tools.create_stock_text_input(state_variable="VaR_alpha",
                                          default_value=0.05,
                                          present_text="VaR Alpha",
                                          key="side_bar_VaR_alpha")
        with col_cVaRAlpha:
            tools.create_stock_text_input(state_variable="cVaR_alpha",
                                          default_value=0.05,
                                          present_text="cVaR Alpha",
                                          key="side_bar_cVaR_alpha")

        st.session_state["run_simulation"] = st.button("Run Simulation",
                                                       key="main_page_run_simulation",
                                                       on_click=tools.click_button("run_simulation"))
        if st.session_state["run_simulation"]:
            st.title("Simulation Results")
else:
    st.title("Simulation Results")
