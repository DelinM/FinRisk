import datetime
import streamlit as st
import yfinance
import datetime as dt
from assets.Collector import InfoCollector


def create_state_variable(key: str, default_value: any) -> None:
    if key not in st.session_state:
        st.session_state[key] = default_value


def create_stock_text_input(state_variable: str,
                            default_value: str,
                            present_text: str,
                            key: str) -> None:
    create_state_variable(state_variable, default_value)

    st.session_state[state_variable] = st.text_input(present_text,
                                                     key=key,
                                                     value=st.session_state[state_variable])


def click_button_sim() -> None:
    st.session_state["run_simulation"] = True
    st.session_state["run_simulation_check"] = True


def click_button_port() -> None:
    st.session_state["load_portfolio"] = True
    st.session_state["load_portfolio_check"] = True
    st.session_state["run_simulation_check"] = False


def preview_stock(session_state_name: str,
                  start_date: datetime.datetime) -> None:
    st.subheader(st.session_state[session_state_name])
    stock = InfoCollector.get_ticker(st.session_state[session_state_name])
    stock_data = InfoCollector.get_history(stock, period=None,
                                           interval='1h',start=start_date, end=dt.datetime.now())


    stock_data = yfinance.download(st.session_state[session_state_name],
                                   start=start_date,
                                   end=dt.datetime.now())
    stock_data = stock_data[['Close']]

    # change index form 0 to end
    stock_data.index = range(0, len(stock_data))

    st.area_chart(stock_data, use_container_width=True, height=250, width=250, color= "#00fa119e")


def create_date_input(state_variable: str,
                      present_text: str,
                      default_value: str,
                      key: str) -> None:
    create_state_variable(state_variable, None)

    st.session_state[state_variable] = st.date_input(present_text, value=default_value, key=key)


def format_currency(number: float) -> str:
    formatted_number = "${:,.2f}".format(number)
    return formatted_number


def create_side_bar_width():
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 500x !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
