import json
from app.medStaff import MedStaffUser
from app.patient import PatientUser
from app.admin import AdminUser
from datetime import datetime
from app.admin_utils import logging
import io
import csv
import re

class Login:
    def __init__(self, data_path="login_data.json"):
        self.data_path = data_path
        self.medical_staff = []
        self.patients = []
        self.admins = []
        self.config_log = []
        self.log_path = "carelog.log"

        self._load_data()

    def _load_data(self):
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)

                for s in data.get("medical_staff", []):
                    medStaff = MedStaffUser(s["username"], s["password"],s["name"],s["specialisation"],s["email"],s["phone_number"])
                    self.medical_staff.append(medStaff)

                for p in data.get("patients", []):
                    patient = PatientUser(p["username"], p["password"], p["name"], p["email"],p["phone_number"])
                    patient.assigned_caretaker = p.get("assigned_caretaker", [])
                    patient.personal_preferences = p.get("personal_preferences", [])
                    patient.clinical_observations = p.get("clinical_observations", [])
                    self.patients.append(patient)

                for a in data.get("admin_staff",[]):
                    admin = AdminUser(a["username"],a["password"])
                    self.admins.append(admin)

        except FileNotFoundError:
            logging.info("Data file not found. Starting with a clean state.")

    def load_log(self):
        try:
            
            pattern = re.compile(r"^(.*?) - (.*?) - (.*)$")

            with open(self.log_path,'r') as f:
                for line in f:
                    match = pattern.match(line.strip())
                    if match:
                        timestamp, level, message = match.groups()
                        self.config_log.append({
                            "timestamp": timestamp,
                            "level": level,
                            "message": message
                        })

            return self.config_log
        except FileNotFoundError:
            print("Log file not found. Starting with a clean state.")

    def export_logs_to_json(self,output_path="exported_logs.json"):
        logs = self.load_log()
        with open(output_path, "w") as f:
            json.dump(logs, f, indent=4)
        print(f"Logs exported to {output_path}")

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
        if not isinstance(username,str) or not isinstance(password,str):
            return
        for patient in self.patients:
            if username.lower() == patient.username.lower() and password.lower() == patient.password.lower():
                return patient

    def check_valid_username_password_medstaff(self, username, password):
        if not isinstance(username,str) or not isinstance(password,str):
            return
        for medstaff in self.medical_staff:
            if username.lower() == medstaff.username.lower() and password.lower() == medstaff.password.lower():
                return medstaff
            
    def check_valid_username_password_admin(self, username, password):
        if not isinstance(username,str) or not isinstance(password,str):
            return
        for admin in self.admins:
            if username.lower() == admin.username.lower() and password.lower() == admin.password.lower():
                return admin

    def find_medstaff_by_username(self, staff_username):
        if not isinstance(staff_username,str):
            return
        
        for medstaff in self.medical_staff:
            if staff_username.lower() == medstaff.username.lower():
                return medstaff
            
    def find_medstaff_by_name(self, staff_name):
        if not isinstance(staff_name,str):
                    return

        if not re.fullmatch(r"[A-Za-z ]+", staff_name.strip()):
            return

        for medstaff in self.medical_staff:
            if staff_name.lower() == medstaff.name.lower():
                return medstaff

    def find_patient_by_username(self, patient_username):
        if not isinstance(patient_username,str):
            return
        for patient in self.patients:
            if patient_username.lower() == patient.username.lower():
                return patient
            
    def find_patient_by_name(self, patient_name):
        if not isinstance(patient_name,str):
            return
        if not re.fullmatch(r"[A-Za-z ]+", patient_name.strip()):
            return
        for patient in self.patients:
            if patient_name.lower() == patient.name.lower():
                return patient

    def input_patient_personal_preference(self, patient_username, recorded_by_username, preference):
        if not isinstance(patient_username,str) or not isinstance(recorded_by_username,str) or not isinstance(preference,str):
            return
        
        patient = self.find_patient_by_username(patient_username)
        if not self.find_patient_by_username(recorded_by_username) or self.find_medstaff_by_username(recorded_by_username):
            return
        
        if not patient:
            return

        if not preference:
            return

        timestamp = datetime.now().isoformat()

        preference_record = {
            "recorded_by": recorded_by_username,
            "entry": preference,
            "timestamp": timestamp
        }

        patient.personal_preferences.append(preference_record)
        logging.info(f"Save patient personal preference record recorded by{recorded_by_username} on {timestamp}")
        self._save_data()
        return True


    def input_patient_clinical_observation(self, patient_username, recorded_by_username,observation):
        if not isinstance(patient_username,str) or not isinstance(recorded_by_username,str) or not isinstance(observation,str):
            return
        
        patient = self.find_patient_by_username(patient_username)
        if not self.find_patient_by_username(recorded_by_username) or self.find_medstaff_by_username(recorded_by_username):
            return
        
        if not patient:
            return

        if not observation:
            return

        timestamp = datetime.now().isoformat()

        clinical_record = {
            "recorded_by": recorded_by_username,
            "entry": observation,
            "timestamp": timestamp
        }

        patient.clinical_observations.append(clinical_record)
        logging.info(f"Save patient clinical observation record recorded by{recorded_by_username} on {timestamp}")
        self._save_data()
        return True
        
    def assign_care_staff(self, patient_username,staff_name):
        if not isinstance(patient_username,str) or not isinstance(staff_name,str):
            return
        
        if not re.fullmatch(r"[A-Za-z ]+", staff_name.strip()):
            return


        patient = self.find_patient_by_username(patient_username)
        if staff_name not in patient.assigned_caretaker:
            patient.assigned_caretaker.append(staff_name)
            logging.info(f"Assigned {staff_name} to {patient_username}.")
            self._save_data()
            return True
        

    def register_new_patient(self,username, password,name, email, phone_number):
        if not all(isinstance(x, str) for x in [username, password, name, email, phone_number]):
            return 
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            return 
        
        if not phone_number.isdigit():
            return

        if not re.fullmatch(r"[A-Za-z ]+", name.strip()):
            return
        
        patient_username_list = self.get_all_patient_usernames()
        patient_email_list = self.get_all_patient_email()
        patient_phone_number_list= self.get_all_patient_phone_number()

        if username in patient_username_list or username == "":
            return
        if email in patient_email_list:
            return
        if not phone_number.isdigit() or phone_number in patient_phone_number_list:
            return
        
        patient = PatientUser(username, password,name,email, phone_number )
        patient.assigned_caretaker = []
        patient.clinical_observations = []
        patient.personal_preferences = []
        self.patients.append(patient)
        logging.info(f"Successfully registered new account for patient {name}.")
        self._save_data()

        return patient
    
    def remove_patient(self,remove_username):
        if not isinstance(remove_username,str):
            return
        patient = self.find_patient_by_username(remove_username)
        if not patient:
            return
        
        self.patients.remove(patient)
        logging.info(f"Successfully removed patient account with {remove_username} username.")
        self._save_data()
        return True
    
    def get_patient_records_staff(self,patient_username):
        if not isinstance(patient_username,str):
            return
        patient = self.find_patient_by_username(patient_username)
        if patient:
            return {
                "personal_preferences": patient.personal_preferences,
                "clinical_observations": patient.clinical_observations
            }
        else:
            return {}
        
    def get_patient_records_patient(self,patient_username):
        if not isinstance(patient_username,str):
            return
        patient = self.find_patient_by_username(patient_username)
        if patient:
            return patient.personal_preferences
    
    def register_staff(self,username, password,name,specialisation, email, phone_number):
        staff_username_list = self.get_all_medstaff_usernames()
        staff_email_list = self.get_all_medstaff_email()
        staff_phone_number_list= self.get_all_medstaff_phone_number()

        if not all(isinstance(x, str) for x in [username, password, name,specialisation, email, phone_number]):
            return 
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            return 
        
        if not phone_number.isdigit():
            return

        if not re.fullmatch(r"[A-Za-z ]+", name.strip()):
            return
        
        
        if not re.fullmatch(r"[A-Za-z ]+", specialisation.strip()):
            return

        if username in staff_username_list:
            return
        if email in staff_email_list:
            return
        if phone_number in staff_phone_number_list:
            return
            
        staff = MedStaffUser(username, password, name, specialisation, email, phone_number)
        self.medical_staff.append(staff)
        logging.info(f"Successfully registered new account for staff {name}.")
        self._save_data()
        return staff
    
    def remove_staff(self, remove_username):
        if not isinstance(remove_username,str):
            return
        staff = self.find_medstaff_by_username(remove_username)
        if not staff:
            return
        
        self.medical_staff.remove(staff)
        logging.info(f"Successfully removed patient account with {remove_username} username.")
        self._save_data()
        return True
    
    def change_patient_user_password(self,username,password,new_password):
        if not all(isinstance(x, str) for x in [username, password,new_password]):
            return
        patient = self.find_patient_by_username(username)
        if not patient:
            return
        
        if password == patient.password and password != new_password:
            patient.password = new_password
            logging.info(f"Patient account {username} has changed their password")
            self._save_data()
            return True
            
        
    def change_medstaff_user_password(self,username,password,new_password):
        if not all(isinstance(x, str) for x in [username, password,new_password]):
            return

        medstaff = self.find_medstaff_by_username(username)
        if not medstaff:
            return
        
        if password == medstaff.password and password != new_password:
            medstaff.password = new_password
            logging.info(f"Medical staff account {username} has changed their password")
            self._save_data()
            return True
        
    def unassign_care_staff(self, patient_username,staff_name):
        if not isinstance(patient_username,str) or not isinstance(staff_name,str):
            return
        patient = self.find_patient_by_username(patient_username)
        if not patient:
            return
    
        if not re.fullmatch(r"[A-Za-z ]+", staff_name.strip()):
                return
         
        if staff_name in patient.assigned_caretaker:
            patient.assigned_caretaker.remove(staff_name)
            logging.info(f"{staff_name} has been unassigned from {patient_username}")
            self._save_data()
            return True
        else:
            return
    
    def list_all_patients(self):
        if not self.patients:
            return []

        patient_data = []

        for patient in self.patients:
            caretakers = patient.assigned_caretaker if patient.assigned_caretaker else ["None"]

            patient_data.append({
                "username": patient.username,
                "password": patient.password,
                "name": patient.name,
                "email":patient.email,
                "phone_number": patient.phone_number,
                "assigned_caretakers": caretakers
            })

        return patient_data
    
    def list_all_medical_staff(self):
        if not self.medical_staff:
            return []

        medical_staff_data = []

        for medstaff in self.medical_staff:

            medical_staff_data.append({
                "username": medstaff.username,
                "password": medstaff.password,
                "name": medstaff.name,
                "specialisation": medstaff.specialisation,
                "email": medstaff.email,
                "phone_number": medstaff.phone_number
            })

        return medical_staff_data
    
    def get_patients_clinical_observations(self,patient_username):
        if not isinstance(patient_username,str):
            return
        patient = self.find_patient_by_username(patient_username)
        if patient:
            return patient.clinical_observations

    
    def export_report(self, kind,username):
        if not isinstance(username,str):
            return
        if not re.fullmatch(r"[A-Za-z ]+", kind.strip()):
                return
        kind = kind.lower()
        kind_list = ["patient data","medical staff data", "patient historical logs", "patient clinical observations", "configuration logs"]

        if kind not in kind_list:
            return
        if kind == "patient data":
            data_to_export = self.list_all_patients()
            headers = ["username","password","name","email","phone_number","assigned_caretakers"]
        elif kind == "medical staff data":
            data_to_export = self.list_all_medical_staff()
            headers =  ["username","password","name","specialisation","email","phone_number","assigned_caretakers"]
        elif kind == "patient historical logs":
            raw_data = self.get_patient_records_staff(username)
            data_to_export = []

            for entry in raw_data.get("personal_preferences", []):
                data_to_export.append({
                    "recorded_by": entry.get("recorded_by", "Unknown"),
                    "entry": entry.get("entry", ""),
                    "timestamp": entry.get("timestamp", "")
                })

            for entry in raw_data.get("clinical_observations", []):
                data_to_export.append({
                    "recorded_by": entry.get("recorded_by", "Unknown"),
                    "entry": entry.get("entry", ""),
                    "timestamp": entry.get("timestamp", "")
                })

            headers = ["recorded_by", "entry", "timestamp"]

        elif kind == "patient clinical observations":
            data_to_export = self.get_patients_clinical_observations(username)
            headers =  ["recorded_by","entry","timestamp"]

        elif kind == "configuration logs":
            self.load_log()
            data_to_export = self.config_log
            headers = ["timestamp", "level", "message"]
        else:
            return None
        
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(headers)

        for row in data_to_export:
            writer.writerow([row.get(h, "") for h in headers])

        return buffer.getvalue()

    def get_all_patient_usernames(self):
        return [patient.username for patient in self.patients]
    
    def get_all_patient_email(self):
        return [patient.email for patient in self.patients]
    
    def get_all_patient_phone_number(self):
        return [patient.phone_number for patient in self.patients]


    def get_all_medstaff_usernames(self):
        return [medstaff.username for medstaff in self.medical_staff]
    
    def get_all_medstaff_email(self):
        return [medstaff.email for medstaff in self.medical_staff]
    
    def get_all_medstaff_phone_number(self):
        return [medstaff.phone_number for medstaff in self.medical_staff]