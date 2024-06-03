import streamlit as st
from lib.menu import menu
from lib.db import open_db_connection
from lib.argon2 import PasswordHasher

# Set the page configuration
st.set_page_config(page_title="Medi-Selfreminder", page_icon="💊", layout="centered")

# Show the navigation menu
menu()

# Create an instance of PasswordHasher
ph = PasswordHasher()

def create_user(username, password, first_name, last_name, gender, birthday, weight, height):
    hashed_pswd = ph.hash(password)
    with open_db_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO users(username, password, first_name, last_name, gender, birthday, weight, height) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (username, hashed_pswd, first_name, last_name, gender, birthday, weight, height))
        conn.commit()
    st.success("Sign up of {} was successfull!".format(username))
    st.switch_page("pages/login.py")

st.subheader("Sign up")

# Collect user details
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
birthday = st.date_input("Birthday")
weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
height = st.number_input("Height (cm)", min_value=0.0, step=0.1)

# Collect login credentials
new_user = st.text_input("Username")
new_password = st.text_input("Password", type='password')

if st.button("SignUp", key='signup_button'):
    if all([new_user, new_password, first_name, last_name, gender, birthday, weight, height]):
        create_user(new_user, new_password, first_name, last_name, gender, birthday, weight, height)
    else:
        st.warning('Please fill in all the fields!')

col1, col2 = st.columns([0.9, 2.65])
with col1:
    st.write("Already have an account?")
with col2:
    st.page_link("pages/login.py", label="Log in here")
        
image_path = "images/tablets_pills_capsules.jpg"
st.image(image_path, use_column_width=True)