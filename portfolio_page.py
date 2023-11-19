import streamlit as st
import stTools as tools
def load_page():

    st.subheader("Portfolio Preview")


    # create 4 columns
    col_stock1, col_stock_2, col_stock_3, col_stock_4 = st.columns(4)

    with col_stock1:
        tools.preview_stock("stock_1_name",
                            start_date=st.session_state.stock_1_purchase_date)

    with col_stock_2:
        tools.preview_stock("stock_2_name",
                            start_date=st.session_state.stock_2_purchase_date)

    with col_stock_3:
        tools.preview_stock("stock_3_name",
                            start_date=st.session_state.stock_3_purchase_date)

    with col_stock_4:
        tools.preview_stock("stock_4_name",
                            start_date=st.session_state.stock_4_purchase_date)
