import streamlit as st

def show_settings_page(manager):
    """
    Handles calling the streamlit library to draw the GUI for the user to modify their settings, specifically to change password.
    """
    st.header("Settings")
    
    st.subheader("Change User Password")
    with st.form("change_password_form"):
        """
        Handles and draws input fields and user input to change password 

        arg : 
            1 - Current Password (string) - User inputted "current password"
            2 - New password (string) - User's desired new password
            3 - Confirm New Password (string) - user repeats the desired new password

        Fields of Input : 
            current_password - for user input of arg 1
            new_password - for user input of arg 2
            confirm_new_password - For user input of arg 3
            change_password_button - GUI for the user to submit the arguments entered in the fields.

        Outputs : 
            Error(s):
                Input for arg1 does not match the saved password in the DB - Output string telling user the password is incorrect
                Input for arg2 matches arg1  - Output string informing the user the passwords cannot be the same
                Input for arg2 does not match arg3 - Output string telling user the inputs for field 2 and field 3 (for arg2 and arg3) do not match
            If no errors occur : 
                Tells the backend function to update the password, output a string informing the user change was successful.
            
        Desired Outcome : 
            User updates password successfully, changing the password in the database, outputs a confirmation string.
        """
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
