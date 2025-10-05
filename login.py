import json
from medStaff import MedStaffUser
from patient import PatientUser
from admin import AdminUser

class Login:
    def __init__(self, data_path="login_data.json"):
        self.data_path = data_path
        self.medical_staff = []
        self.patients = []
        self.admins = []
        self._load_data()

    def _load_data(self):
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)

                for s in data.get("medical_staff", []):
                    medStaff = MedStaffUser(s["username"], s["password"],s["name"])
                    self.medical_staff.append(medStaff)

                for p in data.get("patients", []):
                    patient = PatientUser(p["username"], p["password"])
                    patient.assigned_caretaker = p.get("assigned_caretaker", [])
                    patient.personal_preferences = p.get("personal_preferences", [])
                    patient.clinical_observations = p.get("clinical_observations", [])
                    self.patients.append(patient)

                for a in data.get("admin_staff",[]):
                    admin = AdminUser(a["username"],a["password"])
                    self.admins.append(admin)

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")

    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        data_to_save = {
            "medical_staff": [s.__dict__ for s in self.medical_staff],
            "patients": [p.to_dict() for p in self.patients],
            "admin_staff": [a.__dict__ for a in self.admins]
        }
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def check_valid_username_password_patient(self, username, password):
        for patient in self.patients:
            if username.lower() == patient.username.lower() and password.lower() == patient.password.lower():
                return patient

    def check_valid_username_password_medstaff(self, username, password):
        for medstaff in self.medical_staff:
            if username.lower() == medstaff.username.lower() and password.lower() == medstaff.password.lower():
                return medstaff
            
    def check_valid_username_password_admin(self, username, password):
        for admin in self.admins:
            print(username.lower())
            print(admin.username.lower())
            print(password.lower())
            print(admin.password.lower())
            if username.lower() == admin.username.lower() and password.lower() == admin.password.lower():
                return admin

    def find_medstaff_by_username(self, staff_username):
        for medstaff in self.medical_staff:
            if staff_username.lower() == medstaff.username.lower():
                return medstaff
            
    def find_medstaff_by_name(self, staff_name):
        for medstaff in self.medical_staff:
            if staff_name.lower() == medstaff.name.lower():
                return medstaff

    def find_patient_by_username(self, patient_username):
        for patient in self.patients:
            if patient_username.lower() == patient.username.lower():
                return patient

    def input_patient_personal_preference(self, patient_username, recorded_by):
        patient = self.find_patient_by_username(patient_username)
        
        if not patient:
            print("Error: Patient not found.")
            return False

        preference = input("Please fill in personal preference: ").strip()
        if not preference:
            print("Error: Preference cannot be empty.")
            return False

        import datetime
        timestamp = datetime.datetime.now().isoformat()

        preference_record = {
            "recorded_by": recorded_by,
            "entry": preference,
            "timestamp": timestamp
        }

        patient.personal_preferences.append(preference_record)
        self._save_data()
        print("Success: Personal preference saved.")
        return True


    def input_patient_clinical_observation(self, patient_username, recorded_by):
        observation = input("Please fill in clinical observation: ")
        patient = self.find_patient_by_username(patient_username)
        if patient:
            from datetime import datetime
            patient.clinical_observations.append({
                "recorded_by": recorded_by,
                "entry": observation,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            self._save_data()
            print("Successfully saved clinical observation")
            return 
        
    def assign_care_staff(self, patient_username,staff_username):
        patient = self.find_patient_by_username(patient_username)
        patient.assigned_caretaker.append(staff_username)
        self._save_data()
        print("Success: Personal preference saved.")
        return True

    def register_new_patient(self):
        username = input("Please enter new patient account username: ")
        password = input("Please enter new patient account password")
        patient = PatientUser(username, password)
        patient.assigned_caretaker = []
        patient.clinical_observations = []
        patient.personal_preferences = []

        self.patients.append(patient)
        self._save_data()
        print(f"Success: patient {patient.username} account is created.")

        return patient
    
    def remove_patient(self):
        remove_username = input("Please enter username of patient to be removed: ")
        patient = self.find_patient_by_username(remove_username)
        if not patient:
            print(f"Cant find patient {remove_username}")
            return False
        
        self.patients.remove(patient)
        self._save_data()
        print(f"Success: patient {patient.username} account has been removed.")
        return True
    
    def get_patient_records_staff(self):
        patient_username = input("Please enter patient username:")
        patient = self.find_patient_by_username(patient_username)
        return {
        "personal_preferences": patient.personal_preferences,
        "clinical_observations": patient.clinical_observations
    }

    def get_patient_records_patient(self,patient_username):
        patient = self.find_patient_by_username(patient_username)
        print("personal preferences")
        return patient.personal_preferences
    
    def register_staff(self):
        username = input("Please enter new staff account username: ")
        password = input("Please enter new staff account password")
        name = input("Please enter new staff name")
        staff = MedStaffUser(username, password, name)

        self.medical_staff.append(staff)
        self._save_data()
        return staff
