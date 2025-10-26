import streamlit as st

def show_settings_page(manager):
    st.header("Settings")
    
    st.subheader("Change User Password")
    with st.form("change_password_form"):
        username = st.session_state.username
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_new_password = st.text_input("Confirm New Password", type="password")

        change_password_button = st.form_submit_button("Change Password")

        if change_password_button:

            if st.session_state.role == "medical staff":
                valid_current = manager.check_valid_username_password_medstaff(username, current_password)
            else:
                valid_current = manager.check_valid_username_password_patient(username, current_password)

            if not valid_current:
                st.error("Original password is incorrect.")
                return

            if current_password == new_password:
                st.error("New and old password cannot be the same")
                return

            if new_password != confirm_new_password:
                st.error("New password does not match the confirm password")
                return

            if st.session_state.role == "medical staff":
                result = manager.change_medstaff_user_password(username, current_password, new_password)
            else:
                result = manager.change_patient_user_password(username, current_password, new_password)
                    
            if result:
                st.success("Successfully changed password")
