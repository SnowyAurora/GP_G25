import streamlit as st
import time 
from app.login import Login
from gui.personal_preference import patient_log_management
from gui.admin_account_management import show_admin_account_management_page
from gui.assign_carestaff import show_carestaff_management_page
from gui.user_database import show_user_database_page
from app.admin_utils import backup_data
from gui.user_settings import show_settings_page
from gui.report_pages import show_report_pages

SESSION_TIMEOUT_SECONDS = 600  # 10 minutes timeout

if "manager" not in st.session_state:
    st.session_state.manager = Login("data/login_data.json")

def check_session_timeout():
    """
    Logs out the user automatically if the session has been idle
    for more than SESSION_TIMEOUT_SECONDS.
    """
    current_time = time.time()

    # Initialize last activity timestamp
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = current_time

    # Check for inactivity
    if st.session_state.logged_in:
        elapsed = current_time - st.session_state.last_activity
        if elapsed > SESSION_TIMEOUT_SECONDS:
            st.warning("⚠️ Session timed out due to inactivity.")
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.session_state.username = None
            st.session_state.last_activity = None
            st.rerun()

    # Update last activity timestamp
    st.session_state.last_activity = current_time

def login_page():
    st.title("🔐 Login Page")

    user_type = st.selectbox("User Type", ["Patients", "Medical Staff", "Administrative staff"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Match GUI selection with backend authentication
        if user_type == "Patients":
            try:
                user, message = st.session_state.manager.check_valid_username_password_patient(username, password)
            except:
                user, message = None, "Invalid patient credentials"

        elif user_type == "Medical Staff":
            try:
                user, message = st.session_state.manager.check_valid_username_password_medstaff(username, password)
            except:
                user, message = None, "Invalid medical staff credentials"
        elif user_type == "Administrative staff":
            try:
                user, message = st.session_state.manager.check_valid_username_password_admin(username, password)
            except:
                user, message = None, "Invalid admin credentials"

        # --- Handle account locked with countdown ---
        if isinstance(message, tuple) and message[0] == "locked":
            remaining = message[1]
            st.error("Account locked! Please wait until it’s automatically unlocked.")
            placeholder = st.empty()

            # Display live countdown
            while remaining > 0:
                mins, secs = divmod(remaining, 60)
                timer_str = f"{mins:02d}:{secs:02d}"
                placeholder.warning(f"Unlocks in **{timer_str}**")
                time.sleep(1)
                remaining -= 1

            st.success("✅ Account automatically unlocked! Please try logging in again.")
            st.rerun()  # refresh page after countdown

        # --- Handle successful login ---
        elif user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.session_state.role = user_type
            st.session_state.username = username
            st.success(message)
            st.rerun()

        # --- Handle invalid login ---
        else:
            st.error(message)


def main_app():

    check_session_timeout()  # Run timeout check on every rerun
    st.title("Welcome to CareLog System Dashboard")
    st.write(f"Logged in as **{st.session_state.role}**: {st.session_state.username}")
    st.sidebar.title("CareLog System Navigation")
    st.session_state.role = st.session_state.role.strip().lower()

    if st.session_state.role == "medical staff":
        page = st.sidebar.radio("Go to",["Patient clinical observations and personal logs","Settings"])
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
        if page == "Patient clinical observations and personal logs":
            patient_log_management(st.session_state.manager)
        elif page == "Settings":
            show_settings_page(st.session_state.manager)

    elif st.session_state.role == "patients":
        page = st.sidebar.radio("Go to",["Log management","Settings"])
        if page == "Log management":
            patient_log_management(st.session_state.manager)
        elif page == "Settings":
            show_settings_page(st.session_state.manager)
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
        
    else:
        page = st.sidebar.radio("Go to",["Account Management","Assign Care Staff","User Account Database","Export Reports"])
        st.sidebar.markdown("---")
        if st.sidebar.button("💾 Backup Now"):
            if backup_data():
                st.sidebar.success("✅ Backup completed successfully!")
            else:
                st.sidebar.error("❌ Backup failed. Check logs.")

        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False

        if page == "Account Management":
            show_admin_account_management_page(st.session_state.manager)
        elif page == "Assign Care Staff":
            show_carestaff_management_page(st.session_state.manager)
        elif page == "User Account Database":
            show_user_database_page(st.session_state.manager)
        elif page == "Export Reports":
            show_report_pages(st.session_state.manager)
            


def launch():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False 

    if st.session_state.logged_in:
        st.set_page_config(layout="wide", page_title="CareLog Logging System")

        main_app()
    else:
        login_page()