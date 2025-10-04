import json
from user import User
from medStaff import MedStaffUser
from patient import PatientUser

class Login:
    def __init__(self, data_path="login_data.json"):
        self.data_path = data_path
        self.medical_staff = []
        self.patients = []
        self._load_data()

    def _load_data(self):
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)

                # Load medical staff
                for s in data.get("medical_staff", []):
                    medStaff = MedStaffUser(s["username"], s["password"],s["name"])
                    self.medical_staff.append(medStaff)

                # Load patients (with embedded prefs + obs)
                for p in data.get("patients", []):
                    patient = PatientUser(p["username"], p["password"])
                    patient.assigned_caretaker = p.get("assigned_caretaker", [])
                    patient.personal_preferences = p.get("personal_preferences", [])
                    patient.clinical_observations = p.get("clinical_observations", [])
                    self.patients.append(patient)

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")

    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        data_to_save = {
            "medical_staff": [s.__dict__ for s in self.medical_staff],
            "patients": [p.to_dict() for p in self.patients]  # custom method for nested dicts
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

