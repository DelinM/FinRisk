import pandas as pd
import streamlit as st
import sidebar as comp
import stTools as tools
import Portfolio

st.set_page_config(
    page_title="FinRisk",
    page_icon="🚀",
    layout="wide"
)

st.title("Financial Risk Management Simulation - FinRisk")

comp.load_sidebar()

if "run_simulation" not in st.session_state:
    st.session_state["run_simulation"] = False

if "load_portfolio" not in st.session_state:
    st.session_state["load_portfolio"] = False

if not st.session_state.load_portfolio:
    if st.session_state.run_simulation:
        my_protfolio = Portfolio.Portfolio(init_cash=int(st.session_state.init_cash),
                                           start_date=st.session_state.start_date,
                                           end_date=st.session_state.end_date)
        my_protfolio.add_stock(stock=st.session_state.stock_1_name, weight=float(st.session_state.stock_1_weight))
        my_protfolio.add_stock(stock=st.session_state.stock_2_name, weight=float(st.session_state.stock_2_weight))
        my_protfolio.add_stock(stock=st.session_state.stock_3_name, weight=float(st.session_state.stock_3_weight))
        my_protfolio.add_stock(stock=st.session_state.stock_4_name, weight=float(st.session_state.stock_4_weight))

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
            st.text(f"Portfolio VaR: {my_protfolio.VaR}")

        with col3:
            st.text(f"Portfolio cVaR: {my_protfolio.cVaR}")


        st.subheader("Portfolio Returns")
        st.line_chart(my_portfolio_returns, use_container_width=True, height=500, width=250)


        # convert my_portfolio_returns ndarray to dataframe
        df = pd.DataFrame(my_portfolio_returns)


        st.download_button(label="Download Portfolio Returns",
                            data=df.to_csv(),
                            file_name="Portfolio Returns.csv",
                            mime="text/csv")




    else:
        st.text("Please load portfolio!")

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
    col_monte1, col_monte2 = st.columns(2)

    with col_monte1:
        tools.create_stock_text_input(state_variable="no_simulations",
                                      default_value=100,
                                      present_text="No. of Simulations",
                                      key="main_no_simulations")

        tools.create_stock_text_input(state_variable="VaR_alpha",
                                      default_value=0.05,
                                      present_text="VaR Alpha",
                                      key="side_bar_VaR_alpha")
    with col_monte2:
        tools.create_stock_text_input(state_variable="no_days",
                                      default_value=100,
                                      present_text="No. of Days",
                                      key="main_no_days")

        tools.create_stock_text_input(state_variable="cVaR_alpha",
                                      default_value=0.05,
                                      present_text="cVaR Alpha",
                                      key="side_bar_cVaR_alpha")

    if "run_simulation" not in st.session_state:
        st.session_state["run_simulation"] = False

    st.session_state["run_simulation"] = st.button("Run Simulation",
                                                   key="main_page_run_simulation",
                                                   on_click=tools.click_button("run_simulation"))
    st.session_state["run_simulation"] = True
