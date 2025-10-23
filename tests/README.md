Github link:

The CareLog is a lightweight Python-based software solution designed for hospital staff and patients to log daily notes about patients.

The main features implemented in the CareLog software for each user type include:
Patient:
1. Secure login and logout function
2. Create logs to record personal preference
3. View historical logs for:
    Self logged personal preferences,
    Personal preferences logged by medical staff
4. Change password

Medical Staff
1. Secure login and logout function
2. Create logs for:
    Personal preference for each respective patient
    Clinical observations for each respective patient
3. View each patient's complete historical logs for clinical observations and personal preferences
4. Change password

Administrative staff
1. Secure login and logout function
2. Create and remove existing patient and medical staff user accounts.
3. Assign and unassign care staff to patients
4. View all patient and medical staff data stored in the JSON database file.
5. Export reports for:
    Patient Data,
    Medical Staff Data,
    Patient Historical Logs (personal preference + clinical observations logs),
    Patient Clinical Observations,
    Configuration Logs
6. Peform backup operations by using 'Backup' button in the GUI

To launch the GUI:
1. Run streamlit command in terminal: python -m streamlit run main.py

To run the test cases for unit testing:
1. Run pytest command in terminal : python -m pytest -vv





