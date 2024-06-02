import streamlit as st
from menu import menu_with_redirect
from db import open_db_connection

# Set the page configuration
st.set_page_config(page_title="Medi-Selfreminder", page_icon="💊", layout="centered")

# Show the navigation menu
menu_with_redirect()

st.title("🪪 Profile")
st.header("User information")
st.write("Here you can view your profile.")

with open_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT first_name, last_name, gender, birthday, weight, height FROM users WHERE username = ?', (st.session_state.username,))
        user_info = c.fetchone()
        if user_info:
            first_name, last_name, gender, birthday, weight, height = user_info

            # Custom CSS for styling
            user_info_style = """
            <style>
                .user-info {
                    background-color: #2E2E2E;
                    padding: 20px;
                    border-radius: 10px;
                    color: #FFFFFF;
                }
                .user-info h2 {
                    color: #4CAF50;
                }
                .user-info p {
                    font-size: 18px;
                }
            </style>
            """

            st.markdown(user_info_style, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="user-info">
                    <h2>{first_name} {last_name}</h2>
                    <p><strong>Gender:</strong> {gender}</p>
                    <p><strong>Birthday:</strong> {birthday}</p>
                    <p><strong>Weight:</strong> {weight} kg</p>
                    <p><strong>Height:</strong> {height} cm</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("User information not found.")