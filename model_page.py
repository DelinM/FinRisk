import streamlit as st
import stTools as tools
from models.MonteCarloSimulator import Monte_Carlo_Simulator
import model_page_components


def load_page() -> None:
    my_portfolio = st.session_state.my_portfolio
    # create a monte carlo simulation
    monte_carlo_model = Monte_Carlo_Simulator(cVaR_alpha=st.session_state.cVaR_alpha,
                                              VaR_alpha=st.session_state.VaR_alpha)
    monte_carlo_model.get_portfolio(portfolio=my_portfolio,
                                    start_time=st.session_state.start_date,
                                    end_time=st.session_state.end_date)
    monte_carlo_model.apply_monte_carlo(no_simulations=int(st.session_state.no_simulations),
                                        no_days=int(st.session_state.no_days))

    model_page_components.add_markdown()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Initial Investment")
        # plot initial investment as metric
        book_amount_formatted = tools.format_currency(my_portfolio.book_amount)
        tools.create_metric_card(label="Day 0",
                                 value=book_amount_formatted,
                                 delta=None)

    with col2:
        st.subheader("Simulation Return (VaR)")
        VaR_alpha_formatted = tools.format_currency(monte_carlo_model.
                                                    get_VaR(st.session_state.VaR_alpha))
        tools.create_metric_card(label=f"Day {st.session_state.no_days} with VaR(alpha-{st.session_state.VaR_alpha})",
                                 value=VaR_alpha_formatted,
                                 delta=None)

    with col3:
        st.subheader("Simulation Return (cVaR)")

        cVaR_alpha_formatted = tools.format_currency(monte_carlo_model.
                                                     get_conditional_VaR(st.session_state.cVaR_alpha))
        tools.create_metric_card(label=f"Day {st.session_state.no_days} with cVaR(alpha-{st.session_state.cVaR_alpha})",
                                 value=cVaR_alpha_formatted,
                                 delta=None)

    st.subheader(f"Portfolio Returns after {st.session_state.no_simulations} Simulations")
    model_page_components.add_portfolio_returns_graphs(monte_carlo_model.portfolio_returns)

    # add download button
    model_page_components.add_download_button(monte_carlo_model.portfolio_returns)