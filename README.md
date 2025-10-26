Github link: https://github.com/SnowyAurora/GP_G25

CareLog is a lightweight Python-based software solution designed for hospital staff and patients to log daily notes about patients.

The software is designed to be run on Version 3.13.5 of Python, with the most up to date version of streamlit at time of release.

If neither condition is satisfied, we cannot guaruntee the integrity, functions and stability of the program running on your machine. If any problems or irreversible corruption of your machine occurs, it will be up to you to recover it.

Using The Program :

The program's tested environment of usage is within VSC, with a virtual environment, with streamlit installed. 

To do so : follow the instructions.
    
    1 - Download the entire codebase from github in a zip file
    
    2 - Extract this code to a non c:// root file or write protected file
    
    3 - Open this folder in Visual Studio Code. If you do not have Visual Studio Code, install it.
    
    4 - After opening the code folder in VSC, create a virtual environment and use 3.13.5 as the interpreter/
   
    5 - Install Streamlit, using pip install streamlit in your command terminal.

    Assuming all steps are followed, you may now type :
        python -m streamlit run main.py
    To begin running the program GUI.


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





