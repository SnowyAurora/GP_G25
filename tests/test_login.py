import pytest 
import json
import os
from app.login import Login
from app.admin import AdminUser
from app.patient import PatientUser
from app.medStaff import MedStaffUser

@pytest.fixture
def fresh_login(tmp_path):
    test_data = {
        "medical_staff": [
            {
                "username": "med1",
                "password": "abc123",
                "name": "John Doe",
                "specialisation": "General",
                "email": "johndoe123@gmail.com",
                "phone_number": "0123456789"
            },
            {
                "username": "med2",
                "password": "cbd234",
                "name": "Jane Doe",
                "specialisation": "General",
                "email": "janedoe123@gmail.com",
                "phone_number": "0123456799"
            }
        ],
        "patients": [
            {
                "username": "pat1",
                "password": "pabc123",
                "name": "Peter Doe",
                "email": "peterdoe123@gmail.com",
                "phone_number": "0123456799",
                "assigned_caretaker": [
                    "John Doe"
                ],
                "personal_preferences": [
                    {
                        "recorded_by": "pat1",
                        "entry": "long sleeping hours",
                        "timestamp": "2025-10-15T13:13:39.391249"
                    },
                    {
                        "recorded_by": "med1",
                        "entry": "always sleepy",
                        "timestamp": "2025-10-15T13:14:16.862003"
                    }
                ],
                "clinical_observations": [
                    {
                        "recorded_by": "med1",
                        "entry": "chemo",
                        "timestamp": "2025-10-15T13:14:36.004041"
                    },
                    {
                        "recorded_by": "med1",
                        "entry": "chemo",
                        "timestamp": "2025-10-15T13:14:36.099955"
                    },
                    {
                        "recorded_by": "med1",
                        "entry": "chemo1",
                        "timestamp": "2025-10-15T13:14:41.522353"
                    }
                ]
            },
            {
                "username": "pat2",
                "password": "pcbd234",
                "name": "Joe Doe",
                "email": "joedoe123@gmail.com",
                "phone_number": "0123456799",
                "assigned_caretaker": [],
                "personal_preferences": [],
                "clinical_observations": []
            }
        ],
        "admin_staff": [
            {
                "username": "adm1",
                "password": "aabc123"
            }
        ]
    }

    test_file = tmp_path / "test_login.json"
    with open(test_file, "w") as f:
        json.dump(test_data, f, indent=4)

    return Login(data_path=str(test_file))


def test_load_data_success(fresh_login):
    lg = fresh_login
    assert len(lg.medical_staff) == 2
    assert len(lg.patients) == 2
    assert len(lg.admins) == 1

def test_load_data_fail(tmp_path):
    missing_file = tmp_path / "missing_login.json"
    lg = Login(data_path=str(missing_file))
    result =lg._load_data()
    assert result == None
    assert len(lg.medical_staff) == 0
    assert len(lg.patients) == 0
    assert len(lg.admins) == 0

def test_load_log_valid(tmp_path, fresh_login):
    log_file = tmp_path / "missing_login.json"
    fresh_login.log_path = str(log_file)

    with open(log_file, "w") as f:
        f.write("2025-01-01 - INFO - Test log entry\n")

    logs = fresh_login.load_log()
    assert len(logs) == 1
    assert logs[0]["level"] == "INFO"
    assert logs[0]["message"] == "Test log entry"

def test_load_log_no_file(fresh_login):
    fresh_login.log_path = "nonexistent.log"
    logs = fresh_login.load_log()
    assert logs is None or logs == []

def test_export_logs_to_json(tmp_path, fresh_login):
    log_file = tmp_path / "missing_login.json"
    fresh_login.log_path = str(log_file)

    with open(log_file, "w") as f:
        f.write("2025-01-01 - INFO - Export test log\n")

    export_path = tmp_path / "exported_logs.json"
    fresh_login.export_logs_to_json(output_path=str(export_path))

    assert os.path.exists(export_path)

    with open(export_path, "r") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["message"] == "Export test log"

def test_save_data(fresh_login):
    test_data_path = fresh_login.data_path
    fresh_login._save_data()

    assert os.path.exists(test_data_path)

    with open(test_data_path, "r") as f:
        data = json.load(f)
        assert "patients" in data
        assert "medical_staff" in data
        assert "admin_staff" in data
        assert len(data["patients"]) == 2
        assert len(data["medical_staff"]) == 2
        assert len(data["admin_staff"])== 1

    
def test_check_valid_username_password_patient(fresh_login):
    result = fresh_login.check_valid_username_password_patient("pat1","pabc123")
    assert isinstance(result, PatientUser)
    assert result.username == "pat1"
    assert result.password == "pabc123"

def test_check_valid_username_password_patient_inconsistent_casing(fresh_login):
    result = fresh_login.check_valid_username_password_patient("PaT1","pabc123")
    assert isinstance(result, PatientUser)
    assert result.username == "pat1"
    assert result.password == "pabc123"

def test_check_valid_username_password_patient_invalid_username_type(fresh_login):
    result = fresh_login.check_valid_username_password_patient(1,"pabc1234")
    assert result == None

def test_check_valid_username_password_patient_invalid_password_type(fresh_login):
    result = fresh_login.check_valid_username_password_patient("pat1",1234)
    assert result == None

def test_check_valid_username_password_patient_invalid_password(fresh_login):
    result = fresh_login.check_valid_username_password_patient("pat1","pabc1234")
    assert result == None

def test_check_valid_username_invalid_password_patient_invalid_username(fresh_login):
    result = fresh_login.check_valid_username_password_patient("p4","pabc123")
    assert result == None

def test_check_valid_username_password_patient_invalid(fresh_login):
    result = fresh_login.check_valid_username_password_patient("p4","pabc123567")
    assert result == None

def test_check_valid_username_password_medstaff(fresh_login):
    result = fresh_login.check_valid_username_password_medstaff("med1","abc123")
    assert isinstance(result, MedStaffUser)
    assert result.username == "med1"
    assert result.password == "abc123"

def test_check_valid_username_password_medstaff_inconsistent_casing(fresh_login):
    result = fresh_login.check_valid_username_password_medstaff("Med1","abc123")
    assert isinstance(result, MedStaffUser)
    assert result.username == "med1"
    assert result.password == "abc123"

def test_check_valif_username_password_medstaff_invalid_username_type(fresh_login):
    result = fresh_login.check_valid_username_password_medstaff(1,"abc1234")
    assert result == None

def test_check_valif_username_password_medstaff_invalid_password_type(fresh_login):
    result = fresh_login.check_valid_username_password_medstaff("med1",1234)
    assert result == None

def test_check_valid_username_password_medstaff_invalid_password(fresh_login):
    result = fresh_login.check_valid_username_password_medstaff("med1","abc1234")
    assert result == None

def test_check_valid_username_password_medstaff_invalid_username(fresh_login):
    result = fresh_login.check_valid_username_password_medstaff("4","abc123")
    assert result == None

def test_check_valid_username_password_medstaff_invalid(fresh_login):
    result = fresh_login.check_valid_username_password_medstaff("4","abc123567")
    assert result == None

def test_check_valid_username_password_admin(fresh_login):
    result = fresh_login.check_valid_username_password_admin("adm1","aabc123")
    assert isinstance(result, AdminUser)
    assert result.username == "adm1"
    assert result.password == "aabc123"

def test_check_valid_username_password_admin_inconsistent_casing(fresh_login):
    result = fresh_login.check_valid_username_password_admin("adm1","aabc123")
    assert isinstance(result, AdminUser)
    assert result.username == "adm1"
    assert result.password == "aabc123"

def test_check_valid_username_password_admin_invalid_username_type(fresh_login):
    result = fresh_login.check_valid_username_password_admin(1,"abc1234")
    assert result == None

def test_check_valid_username_password_admin_invalid_password_type(fresh_login):
    result = fresh_login.check_valid_username_password_admin("adm1",1234)
    assert result == None

def test_check_valid_username_password_admin_invalid_password(fresh_login):
    result = fresh_login.check_valid_username_password_admin("adm1","abc1234")
    assert result == None

def test_check_valid_username_password_admin_invalid_username(fresh_login):
    result = fresh_login.check_valid_username_password_admin("4","aabc123")
    assert result == None

def test_check_valid_username_password_admin_invalid(fresh_login):
    result = fresh_login.check_valid_username_password_admin("4","abc123567")
    assert result == None

def test_find_medstaff_by_username(fresh_login):
    result = fresh_login.find_medstaff_by_username("med1")
    assert isinstance(result,MedStaffUser)

def test_find_medstaff_by_username_inconsistent_casing(fresh_login):
    result = fresh_login.find_medstaff_by_username("MeD1")
    assert isinstance(result,MedStaffUser)

def test_find_medstaff_by_username_invalid_type(fresh_login):
    result = fresh_login.find_medstaff_by_username(1)
    assert result == None

def test_find_medstaff_by_username_invalid_username(fresh_login):
    result = fresh_login.find_medstaff_by_username("M1")
    assert result == None

def test_find_medstaff_by_name(fresh_login):
    result = fresh_login.find_medstaff_by_name("john doe")
    assert isinstance(result,MedStaffUser)

def test_find_medstaff_by_name_inconsistent_casing(fresh_login):
    result = fresh_login.find_medstaff_by_name("john Doe")
    assert isinstance(result,MedStaffUser)

def test_find_medstaff_by_name_invalid_type(fresh_login):
    result = fresh_login.find_medstaff_by_name(1)
    assert result == None

def test_find_medstaff_by_name_invalid_name(fresh_login):
    result = fresh_login.find_medstaff_by_name("johhnn doee")
    assert result == None

def test_find_patient_by_username(fresh_login):
    result = fresh_login.find_patient_by_username("pat1")
    assert isinstance(result,PatientUser)

def test_find_patient_by_username_inconsistent_casing(fresh_login):
    result = fresh_login.find_patient_by_username("PaT1")
    assert isinstance(result,PatientUser)

def test_find_patient_by_username_invalid_username_type(fresh_login):
    result = fresh_login.find_patient_by_username(1)
    assert result == None

def test_find_patient_by_username_invalid_username(fresh_login):
    result = fresh_login.find_patient_by_username("ptt1")
    assert result == None

def test_find_patient_by_name(fresh_login):
    result = fresh_login.find_patient_by_name("peter doe")
    assert isinstance(result,PatientUser)

def test_find_patient_by_name_inconsistent_casing(fresh_login):
    result = fresh_login.find_patient_by_name("Peter DOe")
    assert isinstance(result,PatientUser)

def test_find_patient_by_name_invalid_name_type(fresh_login):
    result = fresh_login.find_patient_by_name(1)
    assert result == None

def test_find_patient_by_name_invalid_name(fresh_login):
    result = fresh_login.find_patient_by_name("johhnn doee")
    assert result == None




def test_input_patient_personal_preference(fresh_login):
    result = fresh_login.input_patient_personal_preference("pat1", "pat1","not feeling well")
    assert result == True

def test_input_patient_personal_preference_invalid_patient(fresh_login):
    result = fresh_login.input_patient_personal_preference("p1", "pat1","not feeling well")
    assert result == None

def test_input_patient_personal_preference_invalid_recorder(fresh_login):
    result = fresh_login.input_patient_personal_preference("pat1", "p1","not feeling well")
    assert result == None

def test_input_patient_personal_preference_invalid_patient_type(fresh_login):
    result = fresh_login.input_patient_personal_preference(1, "pat1","not feeling well")
    assert result == None

def test_input_patient_personal_preference_invalid_recorder_type(fresh_login):
    result = fresh_login.input_patient_personal_preference("pat1", 1,"not feeling well")
    assert result == None


def test_input_patient_personal_preference_blank_preference(fresh_login):
    result = fresh_login.input_patient_personal_preference("pat11", "pat1","")
    assert result == None





def test_input_patient_clinical_observation(fresh_login):
    result = fresh_login.input_patient_clinical_observation("pat1", "pat1","not feeling well")
    assert result == True

def test_input_patient_clinical_observation_invalid_patient(fresh_login):
    result = fresh_login.input_patient_clinical_observation("p1", "p1","not feeling well")
    assert result == None

def test_input_patient_clinical_observation_blank_clinical_observation(fresh_login):
    result = fresh_login.input_patient_clinical_observation("p1", "p1","")
    assert result == None

def test_input_patient_clinical_observation_invalid_recorder(fresh_login):
    result = fresh_login.input_patient_clinical_observation("pat1", "m1","not feeling well")
    assert result == None

def test_input_patient_clinical_observation_invalid_patient_type(fresh_login):
    result = fresh_login.input_patient_clinical_observation(1, "med","not feeling well")
    assert result == None

def test_input_patient_clinical_observation_invalid_recorder_type(fresh_login):
    result = fresh_login.input_patient_clinical_observation("pat1", 1,"not feeling well")
    assert result == None



def test_assign_care_staff(fresh_login):
    result = fresh_login.assign_care_staff("pat2","John Doe")
    assert result == True

def test_assign_care_staff_already_assigned(fresh_login):
    result = fresh_login.assign_care_staff("pat1","John Doe")
    assert result == None

def test_assign_care_staff_invalid_patient_type(fresh_login):
    result = fresh_login.assign_care_staff(1,"John Doe")
    assert result == None

def test_assign_care_staff_invalid_staff_type(fresh_login):
    result = fresh_login.assign_care_staff("pat1",1)
    assert result == None


def test_unassign_care_staff(fresh_login):
    result = fresh_login.unassign_care_staff("pat1","John Doe")
    assert result == True

def test_unassign_care_staff_not_assigned(fresh_login):
    result = fresh_login.unassign_care_staff("pat2","John Doe")
    assert result == None

def test_unassign_care_staff_invalid_patient_type(fresh_login):
    result = fresh_login.unassign_care_staff(1,"John Doe")
    assert result == None

def test_unassign_care_staff_invalid_staff_type(fresh_login):
    result = fresh_login.unassign_care_staff("pat2",1)
    assert result == None

def test_register_new_patient(fresh_login):
    result = fresh_login.register_new_patient("pat3","pat3123","Mick Doe", "mk123@gmail.com", "0123999999")
    assert isinstance(result, PatientUser)

def test_register_new_patient_used_username(fresh_login):
    result = fresh_login.register_new_patient("pat1","pat3123","Mick Doe", "mk123@gmail.com", "0123999999")
    assert result == None

def test_register_new_patient_used_email(fresh_login):
    result = fresh_login.register_new_patient("pat3","pat3123","Mick Doe", "joedoe123@gmail.com", "0123999999")
    assert result == None

def test_register_new_patient_used_phone_number(fresh_login):
    result = fresh_login.register_new_patient("pat1","pat3123","Mick Doe", "mk123@gmail.com", "0123456799")
    assert result == None

def test_register_new_patient_invalid_email_format(fresh_login):
    result = fresh_login.register_new_patient("pat3", "pat3123", "Mick Doe", "invalid_email", "0123999999")
    assert result == None

def test_register_new_patient_phone_not_digits(fresh_login):
    result = fresh_login.register_new_patient("pat3", "pat3123", "Mick Doe", "mk123@gmail.com", "01239abc99")
    assert result == None

def test_register_new_patient_invalid_name_characters(fresh_login):
    result = fresh_login.register_new_patient("pat3", "pat3123", "M1ck Doe", "mk123@gmail.com", "0123999999")
    assert result == None

def test_register_new_patient_empty_username(fresh_login):
    result = fresh_login.register_new_patient("", "pat3123", "Mick Doe", "mk123@gmail.com", "0123999999")
    assert result == None


def test_remove_patient(fresh_login):
    result = fresh_login.remove_patient("pat2")
    assert result == True

def test_remove_patient_invalid_username(fresh_login):
    result = fresh_login.remove_patient("1000")
    assert result == None

def test_remove_patient_invalid_username_type(fresh_login):
    result = fresh_login.remove_patient(1000)
    assert result == None




def test_get_patient_records_staff(fresh_login):
    result = fresh_login.get_patient_records_staff("pat1")
    assert isinstance(result, dict)
    assert len(result) == 2

def test_get_patient_records_staff_invalid_username(fresh_login):
    result = fresh_login.get_patient_records_staff("pat4")
    assert result == {}

def test_get_patient_records_staff_invalid_username_type(fresh_login):
    result = fresh_login.get_patient_records_staff(1)
    assert result == None


def test_get_patient_records_patient(fresh_login):
    result = fresh_login.get_patient_records_patient("pat1")
    assert isinstance(result, list)
    assert len(result) == 2

def test_get_patient_records_patient_invalid_patient(fresh_login):
    result = fresh_login.get_patient_records_patient("pat4")
    assert result == None

def test_get_patient_records_patient_invalid_patient_type(fresh_login):
    result = fresh_login.get_patient_records_patient(1)
    assert result == None




def test_register_staff(fresh_login):
    result = fresh_login.register_staff("med3","med3123","Mick Doe","general", "mk123@gmail.com", "0123999999")
    assert isinstance(result, MedStaffUser)
    
def test_register_staff_used_username(fresh_login):
    result = fresh_login.register_staff("med1","med3123","Mick Doe","general", "mk123@gmail.com", "0123999999")
    assert result == None

def test_register_staff_used_email(fresh_login):
    result = fresh_login.register_staff("med3","med3123","Mick Doe","general", "johndoe123@gmail.com", "0123999999")
    assert result == None

def test_register_staff_used_phone_number(fresh_login):
    result = fresh_login.register_staff("med3","med3123","Mick Doe","general", "mk123@gmail.com", "0123456789")
    assert result == None

def test_register_staff_non_string_inputs(fresh_login):
    result = fresh_login.register_staff(
        123, "staffpass", "Mick Doe", "Cardiology", "mickdoe@gmail.com", "0198888888"
    )
    assert result == None

    result = fresh_login.register_staff(
        "staff3", "staffpass", "Mick Doe", 999, "mickdoe@gmail.com", "0198888888"
    )
    assert result == None


def test_register_staff_invalid_email_format(fresh_login):
    result = fresh_login.register_staff(
        "staff3", "staffpass", "Mick Doe", "Cardiology", "invalid_email", "0198888888"
    )
    assert result == None


def test_register_staff_phone_not_digits(fresh_login):
    result = fresh_login.register_staff(
        "staff3", "staffpass", "Mick Doe", "Cardiology", "mickdoe@gmail.com", "01988A8888"
    )
    assert result == None

def test_register_staff_invalid_name_characters(fresh_login):
    result = fresh_login.register_staff(
        "staff3", "staffpass", "M1ck Doe", "Cardiology", "mickdoe@gmail.com", "0198888888"
    )
    assert result == None


def test_register_staff_invalid_specialisation_characters(fresh_login):
    result = fresh_login.register_staff(
        "staff3", "staffpass", "Mick Doe", "Cardiology123", "mickdoe@gmail.com", "0198888888"
    )
    assert result == None


def test_remove_staff(fresh_login):
    result = fresh_login.remove_staff("med1")
    assert result == True

def test_remove_staff_invalid_staff(fresh_login):
    result = fresh_login.remove_staff("med10")
    assert result == None

def test_remove_staff_invalid_staff_type(fresh_login):
    result = fresh_login.remove_staff(1)
    assert result == None



def test_change_patient_user_password(fresh_login):
    result = fresh_login.change_patient_user_password("pat1", "pabc123", "pabc1234")
    assert result == True

def test_change_patient_user_password_invalid_username(fresh_login):
    result = fresh_login.change_patient_user_password("pat10", "pabc123", "pabc1234")
    assert result == None

def test_change_patient_user_password_invalid_password(fresh_login):
    result = fresh_login.change_patient_user_password("pat1", "pacb123", "pabc1234")
    assert result == None

def test_change_patient_user_password_non_string_inputs(fresh_login):
    result = fresh_login.change_patient_user_password(123, "pabc123", "newpass123")
    assert result == None

    result = fresh_login.change_patient_user_password("pat1", "pabc123", 999)
    assert result == None

def test_change_patient_user_password_same_as_old_password(fresh_login):
    result = fresh_login.change_patient_user_password("pat1", "pabc123", "pabc123")
    assert result == None


def test_change_patient_user_password_updates_password_correctly(fresh_login):
    fresh_login.change_patient_user_password("pat2", "pcbd234", "newpass456")
    updated_patient = fresh_login.find_patient_by_username("pat2")
    assert updated_patient.password == "newpass456"



def test_change_medstaff_user_password(fresh_login):
    result = fresh_login.change_medstaff_user_password("med1", "abc123", "abc1234")
    assert result == True

def test_change_medstaff_user_password_invalid_username(fresh_login):
    result = fresh_login.change_medstaff_user_password("med10", "abc123", "abc1234")
    assert result == None

def test_change_medstaff_user_password_invalid_password(fresh_login):
    result = fresh_login.change_medstaff_user_password("med1", "acb123", "abc1234")
    assert result == None

def test_change_medstaff_user_password_non_string_inputs(fresh_login):
    result = fresh_login.change_medstaff_user_password(123, "abc123", "newpass123")
    assert result == None

    result = fresh_login.change_medstaff_user_password("med1", "abc123", 456)
    assert result == None

def test_change_medstaff_user_password_same_as_old_password(fresh_login):
    result = fresh_login.change_medstaff_user_password("med1", "abc123", "abc123")
    assert result == None


def test_change_medstaff_user_password_updates_password_correctly(fresh_login):
    fresh_login.change_medstaff_user_password("med2", "cbd234", "updated456")
    updated_staff = fresh_login.find_medstaff_by_username("med2")
    assert updated_staff.password == "updated456"

def test_list_all_patients(fresh_login):
    result = fresh_login.list_all_patients()
    assert isinstance(result,list)
    assert len(result) == 2

def test_list_all_patients_no_patients(fresh_login):
    fresh_login.remove_patient("pat1")
    fresh_login.remove_patient("pat2")
    result = fresh_login.list_all_patients()
    assert result == []

def test_list_all_medical_staff(fresh_login):
    result = fresh_login.list_all_medical_staff()
    assert isinstance(result,list)
    assert len(result) == 2

def test_list_all_patients_no_patients(fresh_login):
    fresh_login.remove_staff("med1")
    fresh_login.remove_staff("med2")
    result = fresh_login.list_all_medical_staff()
    assert result == []

def test_get_patients_clinical_observations(fresh_login):
    result= fresh_login.get_patients_clinical_observations("pat1")
    assert isinstance(result,list)
    assert len(result) == 3

def test_get_patients_clinical_observations_no_clinical_observations(fresh_login):
    result= fresh_login.get_patients_clinical_observations("pat2")
    assert isinstance(result,list)
    assert len(result) == 0

def test_get_patients_clinical_observations_invalid_patient(fresh_login):
    result= fresh_login.get_patients_clinical_observations("pat3")
    assert result == None

def test_get_patients_clinical_observations_invalid_patient_type(fresh_login):
    result= fresh_login.get_patients_clinical_observations(1)
    assert result == None

def test_export_report_valid_patient_data(fresh_login):
    result = fresh_login.export_report("patient data", "adm1")
    assert isinstance(result, str)
    assert "username,password,name,email,phone_number,assigned_caretakers" in result


def test_export_report_valid_medical_staff_data(fresh_login):
    result = fresh_login.export_report("medical staff data", "adm1")
    assert isinstance(result, str)
    assert "username,password,name,specialisation,email,phone_number,assigned_caretakers" in result


def test_export_report_valid_patient_historical_logs(fresh_login):
    result = fresh_login.export_report("patient historical logs", "pat1")
    assert isinstance(result, str)
    assert "recorded_by,entry,timestamp" in result
    assert "chemo" in result


def test_export_report_valid_patient_clinical_observations(fresh_login):
    result = fresh_login.export_report("patient clinical observations", "pat1")
    assert isinstance(result, str)
    assert "recorded_by,entry,timestamp" in result


def test_export_report_valid_configuration_logs(monkeypatch, fresh_login):
    # Mock load_log and config_log to simulate log loading
    mock_logs = [
        {"timestamp": "2025-10-15T12:00:00", "level": "INFO", "message": "System started"}
    ]

    def mock_load_log():
        fresh_login.config_log = mock_logs

    monkeypatch.setattr(fresh_login, "load_log", mock_load_log)
    result = fresh_login.export_report("configuration logs", "adm1")

    assert isinstance(result, str)
    assert "timestamp,level,message" in result
    assert "System started" in result


def test_export_report_invalid_kind(fresh_login):
    result = fresh_login.export_report("invalid kind", "adm1")
    assert result == None


def test_export_report_invalid_kind_format(fresh_login):
    # Contains digits — invalid because of regex check
    result = fresh_login.export_report("patient123", "adm1")
    assert result == None


def test_export_report_invalid_username_type(fresh_login):
    result = fresh_login.export_report("patient data", 123)
    assert result == None


def test_export_report_empty_kind(fresh_login):
    result = fresh_login.export_report("", "adm1")
    assert result == None


def test_export_report_case_insensitive(fresh_login):
    result = fresh_login.export_report("PaTieNT DaTA", "adm1")
    assert isinstance(result, str)
    assert "username,password,name,email,phone_number,assigned_caretakers" in result

def test_get_all_patient_usernames(fresh_login):
    result = fresh_login.get_all_patient_usernames()
    assert isinstance(result,list)
    assert len(result) == 2

def test_get_all_patient_usernames_no_patients(fresh_login):
    fresh_login.remove_patient("pat1")
    fresh_login.remove_patient("pat2")
    result = fresh_login.get_all_patient_usernames()
    assert isinstance(result,list)
    assert result == []

def test_get_all_patient_email(fresh_login):
    result = fresh_login.get_all_patient_email()
    assert isinstance(result,list)
    assert len(result) == 2

def test_get_all_patient_email_no_patients(fresh_login):
    fresh_login.remove_patient("pat1")
    fresh_login.remove_patient("pat2")
    result = fresh_login.get_all_patient_email()
    assert isinstance(result,list)
    assert result == []

def test_get_all_patient_phone_number(fresh_login):
    result = fresh_login.get_all_patient_phone_number()
    assert isinstance(result,list)
    assert len(result) == 2

def test_get_all_patient_phone_number_no_patients(fresh_login):
    fresh_login.remove_patient("pat1")
    fresh_login.remove_patient("pat2")
    result = fresh_login.get_all_patient_phone_number()
    assert isinstance(result,list)
    assert result == []


def test_get_all_medstaff_usernames(fresh_login):
    result = fresh_login.get_all_medstaff_usernames()
    assert isinstance(result,list)
    assert len(result) == 2

def test_get_all_medstaff_usernames_no_patients(fresh_login):
    fresh_login.remove_staff("med1")
    fresh_login.remove_staff("med2")
    result = fresh_login.get_all_medstaff_usernames()
    assert isinstance(result,list)
    assert result == []

def test_get_all_medstaff_email(fresh_login):
    result = fresh_login.get_all_medstaff_email()
    assert isinstance(result,list)
    assert len(result) == 2

def test_get_all_medstaff_email_no_patients(fresh_login):
    fresh_login.remove_staff("med1")
    fresh_login.remove_staff("med2")
    result = fresh_login.get_all_medstaff_email()
    assert isinstance(result,list)
    assert result == []

def test_get_all_patient_phone_number(fresh_login):
    result = fresh_login.get_all_medstaff_phone_number()
    assert isinstance(result,list)
    assert len(result) == 2

def test_get_all_patient_phone_number_no_patients(fresh_login):
    fresh_login.remove_staff("med1")
    fresh_login.remove_staff("med2")
    result = fresh_login.get_all_medstaff_phone_number()
    assert isinstance(result,list)
    assert result == []









