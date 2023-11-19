import pandas as pd
import streamlit as st
import side_bar as comp
import stTools as tools
from assets import Portfolio
from assets import Stock
from models.MonteCarloSimulator import Monte_Carlo_Simulator
import default_main_page
import portfolio_main_page

st.set_page_config(
    page_title="FinRisk",
    page_icon="🚀",
    layout="wide"
)

tools.remove_white_space()

st.title("Investment Risk Management Simulation")

comp.load_sidebar()

if "load_portfolio_check" not in st.session_state:
    st.session_state["load_portfolio_check"] = False

if "run_simulation_check" not in st.session_state:
    st.session_state["run_simulation_check"] = False

if not st.session_state.load_portfolio_check:
    default_main_page.load_page()

elif not st.session_state.run_simulation_check and st.session_state.load_portfolio_check:
    portfolio_main_page.load_page()

elif st.session_state.run_simulation_check:

    stock_1 = Stock.Stock(stock_name=st.session_state.stock_1_name)
    stock_2 = Stock.Stock(stock_name=st.session_state.stock_2_name)
    stock_3 = Stock.Stock(stock_name=st.session_state.stock_3_name)
    stock_4 = Stock.Stock(stock_name=st.session_state.stock_4_name)

    stock_1.add_buy_action(quantity=int(st.session_state.stock_1_share),
                           purchase_date=st.session_state.start_date)
    stock_2.add_buy_action(quantity=int(st.session_state.stock_2_share),
                           purchase_date=st.session_state.start_date)
    stock_3.add_buy_action(quantity=int(st.session_state.stock_3_share),
                           purchase_date=st.session_state.start_date)
    stock_4.add_buy_action(quantity=int(st.session_state.stock_4_share),
                           purchase_date=st.session_state.start_date)

    my_portfolio = Portfolio.Portfolio()
    my_portfolio.add_stock(stock=stock_1)
    my_portfolio.add_stock(stock=stock_2)
    my_portfolio.add_stock(stock=stock_3)
    my_portfolio.add_stock(stock=stock_4)

    # create a monte carlo simulation
    monte_carlo_model = Monte_Carlo_Simulator(cVaR_alpha=st.session_state.cVaR_alpha,
                                              VaR_alpha=st.session_state.VaR_alpha)
    monte_carlo_model.get_portfolio(portfolio=my_portfolio,
                                    start_time=st.session_state.start_date,
                                    end_time=st.session_state.end_date)
    print(st.session_state.no_simulations)
    monte_carlo_model.apply_monte_carlo(no_simulations=int(st.session_state.no_simulations),
                                        no_days=int(st.session_state.no_days))

    col1, col2, col3 = st.columns(3)

    with col1:
        book_amount_formatted = tools.format_currency(my_portfolio.book_amount)
        st.text(f"Portfolio Initial Investment: {book_amount_formatted}")

    with col2:
        VaR_alpha_formatted = tools.format_currency(monte_carlo_model.
                                                    get_VaR(st.session_state.VaR_alpha))
        st.text(f"Investment with VaR(alpha={st.session_state.VaR_alpha}): "
                f"{VaR_alpha_formatted}")

    with col3:
        cVaR_alpha_formatted = tools.format_currency(monte_carlo_model.
                                                     get_conditional_VaR(st.session_state.cVaR_alpha))
        st.text(f"Investment with cVaR(alpha={st.session_state.cVaR_alpha}): "
                f"{cVaR_alpha_formatted}")

    st.subheader("Portfolio Returns")
    st.line_chart(monte_carlo_model.portfolio_returns, use_container_width=True, height=500, width=250)

    # convert my_portfolio_returns ndarray to dataframe
    df = pd.DataFrame(monte_carlo_model.portfolio_returns)

    col1, col2, col3 = st.columns(3)

    with col3:
        st.download_button(label="Download Portfolio Returns",
                           data=df.to_csv(),
                           file_name="Portfolio Returns.csv",
                           mime="text/csv")
