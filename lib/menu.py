import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.title(f"Welcome {st.session_state.username}! 😊")
    st.sidebar.header("Navigation")
    st.sidebar.page_link("pages/profile.py", label="🪪 Profile")
    st.sidebar.page_link("pages/doctor_insurance.py", label="🩺 Doctor / Insurance")
    st.sidebar.page_link("pages/medicine.py", label="🧾 Medicine")
    st.sidebar.page_link("pages/logout.py", label="🔒 Logout")
    link_text = """
    <div>
        <p>Bei Fragen zu spezifischen Medikamente, klicke <a href="https://compendium.ch/" target="_blank">hier</a>.</p>
    </div>
    """
    st.sidebar.markdown(link_text, unsafe_allow_html=True)
    #<div style="position: fixed; bottom: 0;">

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.title("")
    st.sidebar.header("Navigation")
    st.sidebar.page_link("pages/login.py", label="🔑 Log in")
    st.sidebar.page_link("pages/signup.py", label="📝 Sign up")
    st.sidebar.page_link("pages/profile.py", label="🪪 Profile", disabled=True)
    st.sidebar.page_link("pages/doctor_insurance.py", label="🩺 Doctor / Insurance", disabled=True)
    st.sidebar.page_link("pages/medicine.py", label="🧾 Medicine", disabled=True)


def menu():
    # Determine if a user is logged in or not, then show the correct navigation menu
    if "user_logged_in" not in st.session_state or st.session_state.user_logged_in is False:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to render the navigation menu
    if "user_logged_in" not in st.session_state or st.session_state.user_logged_in is False:
        st.switch_page("pages/login.py")
    menu()