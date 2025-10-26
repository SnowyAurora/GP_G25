import streamlit as st
import pandas as pd

def clean_dataframe(df):
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else x
        )
    return df

def show_user_database_page(manager):
    """
        Draws the GUI for a list of all patients or staff members from the database.

        Args : 
            None
            
        Outputs : 
            Error(s) : 
                No staff users in DB - Outputs string telling user no staff accounts could be found
                No patient users in DB - Outputs string saying no patient accounts could be found
            If no errors occur : 
                Draws a GUI of all staff users or patient users

        Desired Outcome : 
            Draws all users in the database
    """
    st.header("User Database")

    st.subheader("Patient Account Database")
    patients = manager.list_all_patients()
    if patients:
        df_patients = pd.DataFrame(patients)
        df_patients = clean_dataframe(df_patients)
        st.dataframe(df_patients)
    else:
        st.info("No patient accounts found.")

    st.subheader("Medical Staff Account Database")
    staff = manager.list_all_medical_staff()
    if staff:
        df_staff = pd.DataFrame(staff)
        df_staff = clean_dataframe(df_staff)
        st.dataframe(df_staff)
    else:
        st.info("No medical staff accounts found.")
