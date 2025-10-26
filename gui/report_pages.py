import streamlit as st

def show_report_pages(manager):
    """
    Draws the GUI to allow the user to call the backend function to output all data of a desired type in the system.
        Data Types Usable : 
            Patient Users (and associated data)
            Medical Staff Users (and associated data)
            Patient Logs 
            Patient Clinical Observations
            Program Config Logs
    """
    st.subheader("Print Reports")

    report_types = [
        "Patient Data",
        "Medical Staff Data",
        "Patient Historical Logs",
        "Patient Clinical Observations",
        "Configuration Logs"
    ]

    selected_report = st.selectbox("Select Report Type", report_types).lower()

    requires_patient = selected_report in [
        "patient historical logs",
        "patient clinical observations"
    ]
    
    selected_patient = None
    if requires_patient:
        patient_list = manager.get_all_patient_usernames()
        if not patient_list:
            st.warning("No patients available for selection.")
            return
        selected_patient = st.selectbox("Choose a Patient", patient_list)

    if st.button("Export Report"):
        if requires_patient and not selected_patient:
            st.error("Please select a patient before exporting this report.")
            return

        csv_data = manager.export_report(selected_report, selected_patient)

        if csv_data is not None:
            st.download_button(
            label = "Download Report",
            data=csv_data,
            file_name=f"{selected_report}_report.csv",
            mime="text/csv" )
        else:
            st.error("No data available to export")
