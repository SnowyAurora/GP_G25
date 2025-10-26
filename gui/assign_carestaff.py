import streamlit as st

def show_carestaff_management_page(manager):
    """
    Defines functions and methods the user uses to assign or unassign staff to a patient, and draws the associated GUI and Fields needed.
    """
    st.header("Manage carestaff assignment")

    st.subheader("Assign care staff to patient")
    """
    Fetches the patient and staff usernames in the database.
    """
    patient_username_list = manager.get_all_patient_usernames()
    staff_name_list = manager.get_all_medstaff_name()

    if not patient_username_list or not staff_name_list:
        """
            Checks the database for patients or staff, displaying an error message if no staff or patients are found.
            Args : None
            Returns : None
        """
        st.warning("No patients or staff available for assignment.")
        return


    with st.form("assign_form"):
        """
        Allows the user to select staff to assign to a patient.

            Inputs : 
                User Mouse Input

            Error(s) : 
                If user assigns a staff to a patient and the program is unable to assign that staff to the patient - Outputs a string informing the user that the assignment failed.
            
            Desired Outcome : 
                User successfully assigns a staff member to a patient, with a confirmation string outputted confirming the assignment was successful using the staff username and patient username.
        """
        assign_patient_username = st.selectbox("Select patient", patient_username_list)
        assign_staff_username = st.selectbox("Select staff", staff_name_list)
        assign_button = st.form_submit_button("Assign")
    
        if assign_button:
            result_assign = manager.assign_care_staff(assign_patient_username, assign_staff_username)
            if result_assign:
                st.success(f"Assigned {assign_staff_username} to {assign_patient_username}")
            else:
                st.error(f"Unable to assign staff.") 

    st.header("Unassign care staff from patient")
    """
        Allows the user to unassign a staff member from the patient.

            Inputs : 
                User Mouse Input

            Error(s) : 
                If user unassigns a staff to a patient and the program is unable to unassign that staff from the patient - Outputs a string informing the user that the ubassignment failed.
            
            Desired Outcome : 
                User successfully unassigns a staff member to a patient, with a confirmation string outputted confirming the assignment was successful using the staff username and patient username.
        """
    with st.form("unassign_form"):
        unassign_patient_username = st.selectbox("Select patient", patient_username_list)
        unassign_staff_username = st.selectbox("Select staff", staff_name_list)
        unassign_button = st.form_submit_button("Unassign")
    
        if unassign_button:
            result_assign = manager.unassign_care_staff(unassign_patient_username, unassign_staff_username)
            if result_assign:
                st.success(f"Unassigned {unassign_staff_username} from {unassign_patient_username}")
            else:
                st.error(f"Unable to unassign staff.")
