import pandas as pd
import streamlit as st
import sidebar as comp
import stTools as tools
from fin import Portfolio

st.set_page_config(
    page_title="FinRisk",
    page_icon="🚀",
    layout="wide"
)

st.title("Financial Risk Management Simulation - FinRisk")

comp.load_sidebar()

if "load_portfolio_check" not in st.session_state:
    st.session_state["load_portfolio_check"] = False

if "run_simulation_check" not in st.session_state:
    st.session_state["run_simulation_check"] = False

if not st.session_state.load_portfolio_check:
    st.text("👈👈👈Please load portfolio in control panel!")

elif not st.session_state.run_simulation_check and st.session_state.load_portfolio_check:
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

elif st.session_state.run_simulation_check:
    my_protfolio = Portfolio.Portfolio(init_cash=int(st.session_state.init_cash),
                                       start_date=st.session_state.start_date,
                                       end_date=st.session_state.end_date)
    my_protfolio.add_stock(stock=st.session_state.stock_1_name,
                           weight=float(st.session_state.stock_1_weight))
    my_protfolio.add_stock(stock=st.session_state.stock_2_name,
                           weight=float(st.session_state.stock_2_weight))
    my_protfolio.add_stock(stock=st.session_state.stock_3_name,
                           weight=float(st.session_state.stock_3_weight))
    my_protfolio.add_stock(stock=st.session_state.stock_4_name,
                           weight=float(st.session_state.stock_4_weight))

    my_protfolio.get_portfolio_history()
    my_protfolio.apply_monte_carlo(no_simulations=int(st.session_state.no_simulations),
                                   no_days=int(st.session_state.no_days))
    my_protfolio.get_VaR(alpha=float(st.session_state.VaR_alpha))
    my_protfolio.get_conditional_VaR(alpha=float(st.session_state.cVaR_alpha))
    my_portfolio_returns = my_protfolio.portfolio_returns

    col1, col2, col3 = st.columns(3)

    with col1:
        st.text(f"Portfolio Initial Investment: {my_protfolio.init_cash}")

    with col2:
        st.text(f"Portfolio Investment with VaR(alpha={st.session_state.VaR_alpha}): {my_protfolio.VaR}")

    with col3:
        st.text(f"Portfolio Investment with cVaR(alpha={st.session_state.cVaR_alpha}): {my_protfolio.cVaR}")

    st.subheader("Portfolio Returns")
    st.line_chart(my_portfolio_returns, use_container_width=True, height=500, width=250)

    # convert my_portfolio_returns ndarray to dataframe
    df = pd.DataFrame(my_portfolio_returns)

    col1, col2, col3 = st.columns(3)

    with col3:
        st.download_button(label="Download Portfolio Returns",
                           data=df.to_csv(),
                           file_name="Portfolio Returns.csv",
                           mime="text/csv")
