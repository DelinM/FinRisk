import streamlit as st
import yfinance
import datetime as dt


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


def click_button(state_variable: str) -> None:
    st.session_state[state_variable] = True


def preview_stock(session_state_name: str) -> None:
    st.subheader(st.session_state[session_state_name])
    stock_1_data = yfinance.download(st.session_state[session_state_name],
                                     start=dt.datetime.now() - dt.timedelta(days=365),
                                     end=dt.datetime.now())
    stock_data = stock_1_data[['Close']]

    st.line_chart(stock_data, use_container_width=True, height=250, width=250)


def create_date_input(state_variable: str,
                      default_value: str,
                      key: str) -> None:
    create_state_variable(state_variable, None)

    st.session_state[state_variable] = st.date_input("Start Date", value=default_value, key=key)
