import streamlit as st
import pandas as pd

def patient_log_management(manager):
    st.header("📝 Personal Preference Management")

    user_role = st.session_state.role
    current_user = st.session_state.user.username

    # If medical staff, select which patient to record for
    if user_role == "medical staff":
        st.subheader("Select Patient")
        patient_list = manager.get_all_patient_usernames()  
        selected_patient = st.selectbox("Choose a patient", patient_list)
        target_username = selected_patient
        recorded_by = current_user
    else:
        # If patient, record for themselves
        st.subheader("Log Your Personal Preference")
        target_username = current_user
        recorded_by = current_user

    with st.form("personal_preference_form"):
        preference = st.text_input("Enter personal preference")
        submit_btn = st.form_submit_button("Save Preference")

        if submit_btn:
            success = manager.input_patient_personal_preference(
                target_username,
                recorded_by,
                preference
            )
            if success:
                st.success("Preference saved successfully!")
            else:
                st.error("Could not save preference. Check patient/user or text.")

    if user_role == "medical staff":
        st.subheader == "Clinical observation management"
        with st.form("clinical_observation_form"):
            clinical_observation_input = st.text_input("Patient Clinical observation")
            co_submit_btn = st.form_submit_button("Save Clinical Observation")
            
            if co_submit_btn:
                clinical_observation  = manager.input_patient_clinical_observation(
                    target_username,
                    recorded_by,
                    clinical_observation_input
                )
                if clinical_observation:
                    st.success("Clinical observation saved successfully!")
                else:
                    st.error("Could not save clinical observation. Please retry.")

    st.subheader("Patient Log history")
    if user_role == "medical staff":
        result = manager.get_patient_records_staff(target_username)
        personal_preferences = result.get("personal_preferences", [])
        clinical_observations = result.get("clinical_observations", [])
        if personal_preferences and clinical_observations is not None:

            pp_df = pd.DataFrame(personal_preferences)
            if not pp_df.empty:
                pp_df["type"] = "Personal Preference"

            co_df = pd.DataFrame(clinical_observations)
            if not co_df.empty:
                co_df["type"] = "Clinical Observation"

            combined_df = pd.concat([pp_df, co_df], ignore_index=True)
            combined_df = combined_df[["type", "recorded_by", "entry", "timestamp"]]
            st.write(combined_df)
        else:
            st.write("No patient historical logs")

    else:
        result = manager.get_patient_records_patient(target_username)
        result = pd.DataFrame(result)
        st.write(result)