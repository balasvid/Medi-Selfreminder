import streamlit as st
from menu import menu_with_redirect
from db import open_db_connection

# Set the page configuration
st.set_page_config(page_title="Medi-Selfreminder", page_icon="💊", layout="centered")

# Show the navigation menu
menu_with_redirect()

def save_family_doctor(username, doctor_name, doctor_phone, doctor_address):
    with open_db_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO family_doctor(username, doctor_name, doctor_phone, doctor_address) 
            VALUES (?, ?, ?, ?)
        ''', (username, doctor_name, doctor_phone, doctor_address))
        conn.commit()
    st.success("Family doctor information saved successfully!")

def save_health_insurance(username, insurance_name, insurance_number, insurance_card_number, insurance_AHV_number):
    with open_db_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO health_insurance(username, insurance_name, insurance_number, insurance_card_number, insurance_AHV_number) 
            VALUES (?, ?, ?, ?, ?)
        ''', (username, insurance_name, insurance_number, insurance_card_number, insurance_AHV_number))
        conn.commit()
    st.success("Health insurance information saved successfully!")

def get_family_doctor(username):
    with open_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT doctor_name, doctor_phone, doctor_address FROM family_doctor WHERE username = ?', (username,))
        return c.fetchone()

def get_health_insurance(username):
    with open_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT insurance_name, insurance_number, insurance_card_number, insurance_AHV_number FROM health_insurance WHERE username = ?', (username,))
        return c.fetchone()


st.title("🩺 Doctor / Insurance")

username = st.session_state.username
family_doctor_info = get_family_doctor(username)
health_insurance_info = get_health_insurance(username)

if family_doctor_info:
    doctor_name, doctor_phone, doctor_address = family_doctor_info
else:
    doctor_name, doctor_phone, doctor_address = '', '', ''

if health_insurance_info:
    insurance_name, insurance_number, insurance_card_number, insurance_AHV_number = health_insurance_info
else:
    insurance_name, insurance_number, insurance_card_number, insurance_AHV_number = '', '', '', ''

st.header("Family Doctor information")
st.write("Here you'll find the information about your family doctor.")
st.subheader("Enter your family doctor information")

# Collect family doctor information
doctor_name = st.text_input("Doctor's Name", value=doctor_name)
doctor_phone = st.text_input("Doctor's Phone", value=doctor_phone)
doctor_address = st.text_area("Doctor's Address", value=doctor_address)

if st.button("Save Family Doctor information"):
    if doctor_name and doctor_phone and doctor_address:
        save_family_doctor(username, doctor_name, doctor_phone, doctor_address)
    else:
        st.warning('Please fill in all the Family Doctor information fields.')

st.header("Health insurance information")
st.write("Here you'll find the information about your health insurance.")
st.subheader("Enter your health insurance information")

# Collect health insurance information
insurance_name = st.text_input("Insurance Name", value=insurance_name)
insurance_number = st.text_input("Insurance Phone Number", value=insurance_number)
insurance_card_number = st.text_input("Insurance Card Number", value=insurance_card_number)
insurance_AHV_number = st.text_input("Insurance AHV Number", value=insurance_AHV_number)

if st.button("Save Health insurance information"):
    if insurance_name and insurance_number and insurance_card_number and insurance_AHV_number:
        save_health_insurance(username, insurance_name, insurance_number, insurance_card_number, insurance_AHV_number)
    else:
        st.warning('Please fill in all the Health insurance information fields.')