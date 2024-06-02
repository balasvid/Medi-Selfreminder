import streamlit as st

st.session_state.user_logged_in = False
st.session_state.username = None
st.switch_page("pages/login.py")