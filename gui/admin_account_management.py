import streamlit as st
import pandas as pd
import re

def show_admin_account_management_page(manager):
    st.header("Account Actions")

    st.subheader("Register new  patient account")
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


    



