import streamlit as st

def show_carestaff_management_page(manager):
    st.header("Manage carestaff assignment")

    st.subheader("Assign care staff to patient")    
    patient_username_list = manager.get_all_patient_usernames()
    staff_name_list = manager.get_all_medstaff_names()

    if not patient_username_list or not staff_name_list:
        st.warning("No patients or staff available for assignment.")
        return


    with st.form("assign_form"):
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
    with st.form("unassign_form"):
        unassign_patient_username = st.selectbox("Select patient", patient_username_list)
        unassign_staff_username = st.selectbox("Select staff", staff_name_list)
        unassign_button = st.form_submit_button("Assign")
    
        if unassign_button:
            result_assign = manager.unassign_care_staff(unassign_patient_username, unassign_staff_username)
            if result_assign:
                st.success(f"Unassigned {unassign_staff_username} from {unassign_patient_username}")
            else:
                st.error(f"Unable to unassign staff.")
