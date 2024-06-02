import streamlit as st
from menu import menu
from db import open_db_connection

# Create tables if they don't exist
with open_db_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users(
                username TEXT PRIMARY KEY,
                password TEXT,
                first_name TEXT,
                last_name TEXT,
                gender TEXT,
                birthday DATE,
                weight REAL,
                height REAL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS medication(
                username TEXT,
                name TEXT,
                dosage TEXT,
                day TEXT,
                time TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS family_doctor(
                username TEXT PRIMARY KEY,
                doctor_name TEXT,
                doctor_phone TEXT,
                doctor_address TEXT,
                FOREIGN KEY(username) REFERENCES users(username)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS health_insurance(
                username TEXT PRIMARY KEY,
                insurance_name TEXT,
                insurance_number TEXT,
                insurance_card_number REAL,
                insurance_AHV_number TEXT,
                FOREIGN KEY(username) REFERENCES users(username)
            )
        ''')
        conn.commit()

# Set the page configuration
st.set_page_config(page_title="Medi-Selfreminder", page_icon="💊", layout="centered")

# Title of the app
st.title('Medi-Selfreminder💊')

def main():

    # Initialize st.session_state.user to None
    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False

    menu()
    
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    
    if 'edit_data' not in st.session_state:
        st.session_state.edit_data = None

    if 'username' not in st.session_state:
        st.session_state.username = None

    st.switch_page("pages/login.py")


if __name__ == "__main__":
    main()