import streamlit as st
from menu import menu
from db import open_db_connection
from passlib.hash import sha256_crypt

# Set the page configuration
st.set_page_config(page_title="Medi-Selfreminder", page_icon="💊", layout="centered")

# Show the navigation menu
menu()

if 'username' not in st.session_state:
    st.session_state.username = None

def login_user(username, password):
    with open_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        data = c.fetchone()
        if data is None:
            st.error("Invalid Username/Password")
        else:
            if sha256_crypt.verify(password, data[1]):
                st.success("Logged In as {}".format(username))
                st.session_state.initial_notification = False
                st.session_state.user_logged_in = True
                st.session_state.username = username
                st.switch_page("pages/medicine.py")
                #st.session_state.page = 'Home'
                #st.rerun()
            else:
                st.error("Invalid Username/Password")

st.subheader("Log in")
username = st.text_input("Username")
password = st.text_input("Password", type='password')
if st.button("Log In", key='login_button'):
    if username and password:
        login_user(username, password)
    else:
        st.warning('Please fill in all the fields!')

col1, col2 = st.columns([1.9, 6.3])
with col1:
    st.write("Don't have an account?")
with col2:
    #if st.button("Sign up for Medi-Selfreminder"):
    #    st.switch_page("pages/signup.py")
    st.page_link("pages/signup.py", label="Sign up for Medi-Selfreminder")

image_path = "images/tablets_pills_capsules.jpg"
st.image(image_path, use_column_width=True)