import streamlit as st
import stTools as tools
from models.MonteCarloSimulator import Monte_Carlo_Simulator
import pandas as pd


def load_page() -> None:
    my_portfolio = st.session_state.my_portfolio
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
        st.subheader("Day 0")
        # plot inital investment as metric
        book_amount_formatted = tools.format_currency(my_portfolio.book_amount)
        tools.create_metric_card(label="Initial Investment",
                                 value=book_amount_formatted,
                                 delta=None)


    with col2:
        st.subheader(f"Day {st.session_state.no_days} with VaR(alpha={st.session_state.VaR_alpha})")
        VaR_alpha_formatted = tools.format_currency(monte_carlo_model.
                                                    get_VaR(st.session_state.VaR_alpha))
        tools.create_metric_card(label="Investment Value",
                                 value=VaR_alpha_formatted,
                                 delta=None)
        # VaR_alpha_formatted = tools.format_currency(monte_carlo_model.
        #                                             get_VaR(st.session_state.VaR_alpha))
        # st.text(f"Investment with VaR(alpha={st.session_state.VaR_alpha}): "
        #         f"{VaR_alpha_formatted}")

    with col3:
        st.subheader(f"Day {st.session_state.no_days} with cVaR(alpha={st.session_state.VaR_alpha})")

        cVaR_alpha_formatted = tools.format_currency(monte_carlo_model.
                                                     get_conditional_VaR(st.session_state.cVaR_alpha))
        tools.create_metric_card(label="Investment Value",
                                    value=cVaR_alpha_formatted,
                                    delta=None)

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
