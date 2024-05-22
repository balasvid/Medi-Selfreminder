import streamlit as st
import pandas as pd
from passlib.hash import sha256_crypt
import sqlite3
import datetime

# Connect to SQLite database
conn = sqlite3.connect('mediselfreminder.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS medication(username TEXT, name TEXT, dosage TEXT, day TEXT, time TEXT)')
conn.commit()

# Title of the app
st.title('Medi-Selfreminder💊')

# Function to display the sidebar menu
def sidebar_menu():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.sidebar.title(f"Welcome {st.session_state.username}! 😊")
    st.sidebar.header("Navigation")
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button('Home', key='home'):
                st.session_state.page = 'Home'
        with col2:
            if st.button('Logout', key='logout'):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.page = 'Login'
                st.rerun()
    else:
        st.write("Please log in to view and add medication.")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button('Login', key='login'):
                st.session_state.page = 'Login'
        with col2:
            if st.button('SignUp', key='signup'):
                st.session_state.page = 'SignUp'

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'Login'
    
    sidebar_menu()
    
    # Page display logic
    if st.session_state.page == 'Home':
        home_page()
    elif st.session_state.page == 'Login':
        login_page()
    elif st.session_state.page == 'SignUp':
        signup_page()

def home_page():
    
    display_medication(st.session_state.username)
    
    # Define the radio button options
    DaysOptions = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    TimeOptions = ['Morning','Noon','Evening','Night']

    # User inputs
    medicine_name = st.sidebar.text_input('Enter the name of the medicine')
    dosage_amount = st.sidebar.text_input('Enter the dosage')
    selected_DaysOption = st.sidebar.selectbox('Select a day:', DaysOptions)
    selected_TimeOption = st.sidebar.selectbox('Select a time:', TimeOptions)       

    # Button to add medicine to the list
    if st.sidebar.button('Add medicine to list', key='add_medicine'):
        if medicine_name and dosage_amount and selected_DaysOption and selected_TimeOption:
            c.execute('INSERT INTO medication(username, name, dosage, day, time) VALUES (?,?,?,?,?)', 
                        (st.session_state.username, medicine_name, dosage_amount, selected_DaysOption, selected_TimeOption))
            conn.commit()
            st.rerun()
        else:
            st.sidebar.warning('Please fill in all the fields!')
        

def login_page():
    st.sidebar.subheader("Login Section")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.button("Login", key='login_button'):
        if username and password:
            login_user(username, password)
        else:
            st.sidebar.warning('Please fill in all the fields!')

def signup_page():
    st.sidebar.subheader("Create New Account")
    new_user = st.sidebar.text_input("Username")
    new_password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.button("SignUp", key='signup_button'):
        if new_user and new_password:
            create_user(new_user, new_password)
        else:
            st.sidebar.warning('Please fill in all the fields!')

def create_user(username, password):
    hashed_pswd = sha256_crypt.hash(password)
    c.execute('INSERT INTO users(username, password) VALUES (?,?)', (username, hashed_pswd))
    conn.commit()
    st.sidebar.success("Sign up of {} was successfull!".format(username))

def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    data = c.fetchone()
    if data is None:
        st.sidebar.error("Invalid Username/Password")
    else:
        if sha256_crypt.verify(password, data[1]):
            st.sidebar.success("Logged In as {}".format(username))
            st.session_state.logged_in = True
            st.session_state.initial_notification = False
            st.session_state.username = username
            st.session_state.page = 'Home'
            st.rerun()
        else:
            st.sidebar.error("Invalid Username/Password")

def display_medication(username):
    #Display the medication DataFrame in the app
    c.execute('SELECT name, dosage, day, time FROM medication WHERE username = ?', (username,))
    data = c.fetchall()
    if data:
        # Convert the data to a DataFrame
        df = pd.DataFrame(data, columns=['Name', 'Dosage', 'Day', 'Time'])

        # Display column headers
        cols = st.columns([1, 1, 1, 1, 1])  # Add an extra column for the delete button
        cols[0].subheader('Name')
        cols[1].subheader('Dosage')
        cols[2].subheader('Day')
        cols[3].subheader('Time')
        cols[4].subheader('Action')  # Header for the delete button column

        # Iterate over the DataFrame and display each row with a delete button
        for i in df.index:
            row_data = df.loc[i]
            cols = st.columns([1, 1, 1, 1, 1])  # Add an extra column for the delete button
            cols[0].text(row_data['Name'])
            cols[1].text(row_data['Dosage'])
            cols[2].text(row_data['Day'])
            cols[3].text(row_data['Time'])
            if cols[4].button('Delete', key=str(i)):
                # Delete the row from the database
                c.execute('DELETE FROM medication WHERE username = ? AND name = ? AND dosage = ? AND day = ? AND time = ?', 
                          (username, row_data['Name'], row_data['Dosage'], row_data['Day'], row_data['Time']))
                conn.commit()
                # Refresh the page after deleting a row to update the table
                st.rerun()
            
            if not st.session_state.initial_notification:
                # Check if the day matches the current day
                current_day = datetime.datetime.now().strftime('%A')
                if row_data['Day'] == current_day:
                    if row_data['Time'] == "Morning" or row_data['Time'] == "Evening":
                        st.toast(f"Don't forget to take {row_data['Dosage']} of {row_data['Name']} in the {row_data['Time']}")
                    else:
                        st.toast(f"Don't forget to take {row_data['Dosage']} of {row_data['Name']} at {row_data['Time']}")
        
        st.session_state.initial_notification = True

    else:
        st.write("No medication data to display.")

if __name__ == "__main__":
    main()
