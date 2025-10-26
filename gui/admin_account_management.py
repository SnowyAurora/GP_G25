import streamlit as st
import pandas as pd
import re

def show_admin_account_management_page(manager):
    """
    Draws the GUI for the admin's account management tab, and handles all input in fields provided in the tab.
    """
    st.header("Account Actions")

    st.subheader("Register new  patient account")
    """
    Allows the admin to register a new patient through the GUI.
    args : 
        new_username (String) : User Input of New Patient's Username
        new_password (String) : User Input of New Patient's Password
        new_name (String) : User Input of New Patient's Real Name
        new_email (String) : User Input of New Patient's Email address
        new_phone (String) : User Input of New Patient's phone number

    Outputs :
        Errors : 
            Bad Input : 
                (Lacks full input of all fields) - Error message telling user to fill in all fields
                (new_name has numeric values) - Error message informing user the name must not contain any numbers
                (new_phone is not composed entirely of numeric values) - Error message informing user to only input numeric values in the field
                (new_email address does NOT match an email address format) - Error message informing user to input a valid email address

            Good Input BUT overlapping values with a different patients username, email or address :
                (Overlapping Usernames) - Inform user that the username is used by another in the patient database, and to input a different username.
                (Overlapping Email address) - Informs user that the email address matches another in the patient database and a different one must be used.
                (Overlapping phone numbers) - Informs user that the phone number matches another in the patient database, and a different one must be used.

            If all inputs are OK but the program cannot save the new user into the database : 
                Outputs a string informing that the application was unable to register the patient.
        
        If all goes well :
            Program outputs a string informing the user that the patient has been successfully registered in the database.

    Desired Outcome : 
        If no errors occur, the program generates a new entry in the database with the inputted information.
    """
    with st.form("register_patient_form"):
        new_username = st.text_input("New Account Username")
        new_password = st.text_input("New Account Password")
        new_name = st.text_input("Real Name (as per Government ID)")
        new_email = st.text_input("Email")
        new_phone = st.text_input("Phone Number")

        register_patient_button = st.form_submit_button("Register")

        if register_patient_button:
            if not new_username or not new_password or not new_name or not new_email or not new_phone:
                st.error("All fields are required.")

            elif any(char.isdigit() for char in new_name):
                st.error("Name should not contain any numbers.")

            elif not new_phone.isdigit():
                st.error("Phone number should contain digits only.")

            elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", new_email):
                st.error("Please enter a valid email address.")

            else:
                existing_usernames = manager.get_all_patient_usernames()
                existing_emails = manager.get_all_patient_email()
                existing_phones = manager.get_all_patient_phone_number()

                if new_username in existing_usernames:
                    st.error("This username is already taken. Please choose another.")
                
                elif new_email in existing_emails:
                    st.error("This email is already registered. Please use another email.")
                
                elif new_phone in existing_phones:
                    st.error("This phone number is already registered. Please use another phone number.")
                
                else:
                    result_register_patient = manager.register_new_patient(
                        new_username, new_password, new_name, new_email, new_phone
                    )

                    if result_register_patient:
                        st.success("Successfully registered!")
                    else:
                        st.error("Unable to register account. Please try again.")


    st.subheader("Remove patient account")
    """
        Allows the admin to remove a patient's account through the account management GUI.

    Args : 
        remove_username - user input username of the patient user to be removed
        remove_patient_confirmation - User Input of "CONFIRM"

    Outputs :
        Errors : 
            Bad Input : 
                (remove_patient_confirmation does not match "CONFIRM") - Outputs error message telling user to enter CONFIRM into the arg field.

            If all inputs are OK but the program cannot delete the user from the database : 
                Outputs a string informing that the application was unable to remove the patient.
        
        If all goes well :
            Program outputs a string informing the user that the patient has been successfully removed from the database.

    Desired Outcome : 
        If no errors occur, the program will remove the patient from the database, and all its associated information.
    """
    with st.form("remove_patient_form"):
        remove_username = st.text_input("Account username to remove")
        remove_patient_confirmation = st.text_input("Please type CONFIRM to confirm remove")

        remove_button = st.form_submit_button("Remove")
        if remove_button:
            if remove_patient_confirmation != "CONFIRM":
                st.error("Please type CONFIRM in the blank space provided")
            else:
                result_patient_remove = manager.remove_patient(remove_username)
                if result_patient_remove:
                    st.success("Successfully removed!")
                else:
                    st.error("Unable to remove account. Please try again!")

    st.subheader("Register Staff")
    """    
        Allows the admin to initialize and register a new staff account through the account management GUI.
    Args : 
        new_staff_username (String) : User Input of New Staff Member's Username
        new_staff_password (String) : User Input of New Staff Member's Password
        new_staff_name (String) : User Input of New Staff Member's Real Name
        new_staff_specialization : User Input of New Staff Member's Specialization
        new_staff_email (String) : User Input of New Staff Member's Email address
        new_staff_phone (String) : User Input of New Staff Member's phone number

    Outputs :
        Errors : 
            Bad Input : 
                (Lacks full input of all fields) - Error message telling user to fill in all fields
                (new_staff_name has numeric values) - Error message informing user the name must not contain any numbers
                (new_staff_specialization has numeric values within) - Error message informing the user the specialization should not contain numeric values
                (new_staff_phone is not composed entirely of numeric values) - Error message informing user to only input numeric values in the field
                (new_staff_email does NOT match an email address format) - Error message informing user to input a valid email address
                
            Good Input BUT overlapping values with a different staff's username, email or address :
                (Overlapping Usernames) - Inform user that the username is used by another staff user in the database, and to input a different username.
                (Overlapping Email address) - Informs user that the email address matches another staff user in the database and a different one must be used.
                (Overlapping phone numbers) - Informs user that the phone number matches another staff user in the database, and a different one must be used.
                
            If all inputs are OK but the program cannot save the new staff user into the database : 
                Outputs a string informing that the application was unable to register the new staff.
        
        If all goes well :
            Program outputs a string informing the user that a staff user has been successfully initialized in the database as an account.

    Desired Outcome : 
        If no errors occur, the program generates a new entry in the database with the inputted information.
    """
    with st.form("register_new_staff_form"):
        new_staff_username = st.text_input("New Account Username")
        new_staff_password = st.text_input("New Account Password")
        new_staff_name = st.text_input("Real Name (as per Government ID)")
        new_staff_specialisation = st.text_input("Specialisation")
        new_staff_email = st.text_input("Email")
        new_staff_phone = st.text_input("Phone Number")

        register_staff_button = st.form_submit_button("Register")

        if register_staff_button:
            if not new_staff_username or not new_staff_password or not new_staff_name or not new_staff_email or not new_staff_phone or not new_staff_specialisation:
                st.error("All fields are required.")

            elif any(char.isdigit() for char in new_staff_name):
                st.error("Name should not contain any numbers.")

            elif any(char.isdigit() for char in new_staff_name):
                st.error("Specialisation should not contain any numbers.")

            elif not new_staff_phone.isdigit():
                st.error("Phone number should contain digits only.")

            elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", new_staff_email):
                st.error("Please enter a valid email address.")

            else:
                existing_staff_usernames = manager.get_all_medstaff_usernames()
                existing_staff_emails = manager.get_all_medstaff_email()
                existing_staff_phones = manager.get_all_medstaff_phone_number()

                if new_staff_username in existing_staff_usernames:
                    st.error("This username is already taken. Please choose another.")

                elif new_staff_email in existing_staff_emails:
                    st.error("This email is already registered. Please use another email.")

                elif new_staff_phone in existing_staff_phones:
                    st.error("This phone number is already registered. Please use another phone number.")

                else:
                    result_register_staff = manager.register_staff(
                        new_staff_username, new_staff_password, new_staff_name, new_staff_email, new_staff_phone
                    )

                    if result_register_staff:
                        st.success("Successfully Registered")
                    else:
                        st.error("Unable to register account. Please try again")


    st.subheader("Remove Staff")
    """
        Allows the admin to remove a staff user's account through the account management GUI.

    Args : 
        remove_staff_username (string) - User Input of username of the staff user to remove
        remove_staff_confirmation (string) - User Input of CONFIRM

    Outputs :
        Errors : 
            Bad Input : 
                (remove_staff_confirmation input does not match "CONFIRM") - Outputs error message telling user to enter CONFIRM into the arg field.

            If all inputs are OK but the program cannot delete the user from the database : 
                Outputs a string informing that the application was unable to remove the user.
        
        If all goes well :
            Program outputs a string informing the user that the staff user has been successfully removed from the database.

    Desired Outcome : 
        If no errors occur, the program removes the staff user from the database, and deletes all associated information with that user.
    """
    with st.form("remove_staff_form"):
        remove_staff_username = st.text_input("Account username to remove")
        remove_staff_confirmation = st.text_input("Please type CONFIRM to confirm remove")

        remove_staff_button = st.form_submit_button("Remove")
        
        if remove_staff_button:
            if remove_staff_confirmation != "CONFIRM":
                st.error("Please type CONFIRM in the blank field provided")
            else:
                result_remove_staff = manager.remove_staff(remove_staff_username)
                if result_remove_staff:
                    st.success("Succesfully removed")
                else:
                    st.error("Unable to remove account. Please try again")


    



